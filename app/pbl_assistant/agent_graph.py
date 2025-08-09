import logging
import sys
from typing import Dict, Any, List, Optional
from typing_extensions import Annotated, TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from pydantic_ai.messages import ModelMessage, ModelMessagesTypeAdapter
from pydantic import ValidationError
from pydantic_ai.exceptions import UnexpectedModelBehavior
import logfire
import asyncio
import os
from app.pbl_assistant.models.profiling import ProjectOption
import re
from datetime import datetime, timezone
import certifi

# Get certifi CA bundle path
CA = certifi.where()

# Make MongoDB optional
try:
    from motor.motor_asyncio import AsyncIOMotorClient
except Exception as e:
    AsyncIOMotorClient = None
    logging.getLogger(__name__).warning("Motor not available, saving to Mongo will be disabled: %s", e)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import your existing agent functions
# from app.pbl_assistant.agents.profiling_agent import create_project_profile
from app.pbl_assistant.agents.info_gathering_agent import info_gathering_agent
from app.pbl_assistant.agents.standards_agent import standards_agent
from app.pbl_assistant.agents.knowledge_graph_agent import kg_agent
from app.pbl_assistant.agents.design_options_agent import design_options_agent

# Import your models
from app.pbl_assistant.models.profiling import (
    StandardsAlignment,
    KnowledgeGraphResult,
    ProjectOptionsResult,
    ProjectDetails,
    ProjectDesignContext,
    ContextualStandard
)

from app.pbl_assistant.localization import LANG_CODE_MAP, translate_text, get_preset, localize

# Use environment variables for MongoDB connection
ATLAS_URI = os.getenv("ATLAS_URI", "mongodb+srv://erandDevbd:oPDTDscngZ6geaAX@cluster0-ea24.kwhgj0v.mongodb.net/")
ATLAS_DB = os.getenv("ATLAS_DB", "erandiapp")

# Initialize MongoDB client and collections
_mongo_client = None
_mongo_db = None
_templates_col = None

# Only initialize if AsyncIOMotorClient is available
if AsyncIOMotorAsyncClient := AsyncIOMotorClient:  # guard aliasing
    try:
        _mongo_client = AsyncIOMotorAsyncClient(
            ATLAS_URI,
            tlsCAFile=CA,
            connectTimeoutMS=20000,
            serverSelectionTimeoutMS=20000,
        )
        if _mongo_client is not None:
            _mongo_db = _mongo_client[ATLAS_DB]
            if _mongo_db is not None:
                _templates_col = _mongo_db["project_templates"]
                # Test connection
                logger.info("MongoDB connection initialized successfully")
    except Exception as e:
        logger.warning("Failed to initialize MongoDB connection: %s", e)


# Define the state for our graph
class PBLState(TypedDict, total=False):
    # Chat messages and travel details
    user_input: str
    messages: Annotated[List[bytes], lambda x, y: x + y]
    project_details: Dict[str, Any]

    # User preferences -> class profile
    # class_profile: ClassProfile
    class_profile: str
    language: NotRequired[str]

    # Results from each agent
    standards_result: StandardsAlignment
    knowledge_graph_result: KnowledgeGraphResult

    # Final options
    project_options: ProjectOptionsResult

    # User selected option
    user_selected_option: Optional[int]

    # Session ID
    session_id: Optional[str]


# Info gathering node
async def gather_info(state: PBLState, writer) -> Dict[str, Any]:
    logger.debug("ENTERING gather_info…")

    # 1) Lang codes
    lang = state.get("language", "English")
    tgt = LANG_CODE_MAP.get(lang, "en")
    src = "en"

    # 2) User→English
    raw = state.get("user_input", "")
    # Coerce a string: cuando venimos de interrupt() puede venir un dict/None
    if not isinstance(raw, str):
        try:
            raw = raw.get("text") if isinstance(raw, dict) else str(raw)
        except Exception:
            raw = ""
    raw = (raw or "").strip()
    user_input = translate_text(raw, tgt, src) if (tgt != src and raw) else raw
    # Nunca envíes texto vacío a Bedrock
    if not user_input:
        user_input = "continue"

    # 3) History
    msgs: List[ModelMessage] = []
    for chunk in state.get("messages", []):
        try:
            parsed = ModelMessagesTypeAdapter.validate_json(chunk)
            for m in parsed:
                # Filtra mensajes sin texto
                text = getattr(m, "content", None)
                if isinstance(text, str) and text.strip():
                    msgs.append(m)
        except Exception:
            # Si un chunk está corrupto, lo saltamos
            continue

    # 4) Slot‐fill
    # Solo pasa history si hay algo útil
    history = msgs if len(msgs) > 0 else None
    async with info_gathering_agent.run_stream(user_input, message_history=history) as result:
        curr = ""
        async for msg, last in result.stream_structured(debounce_by=0.01):
            try:
                parsed = await result.validate_structured_result(msg, allow_partial=True)
            except ValidationError:
                continue
            if parsed and parsed.response:
                delta = parsed.response[len(curr):]
                if delta.strip():
                    writer(localize(delta, src, tgt))
                    curr = parsed.response

        # 5) Merge
        final = await result.get_data()

    prior = state.get("project_details", {}) or {}
    merged = {
        **prior,
        **{k: v for k, v in final.model_dump().items() if v not in (None, "", [])}
    }

    # 6) Missing?
    missing = [
        name
        for field, name in [
            ("topic", "topic"),
            ("grade_level", "grade level"),
            ("duration_preference", "duration"),
        ]
        if not str(merged.get(field, "")).strip()
    ]

    # 7) Prompt
    if missing:
        merged["all_details_given"] = False
        base = get_preset("need_more_info", lang)
        ask = get_preset("provide_missing_slots", lang).format(slots=", ".join(missing))
        prompt = f"{base} {ask}"
    else:
        merged["all_details_given"] = True
        prompt = get_preset("all_info_received", lang)

    # because get_preset already returns localized text, no localize() here:
    writer("\n" + prompt)

    # 8) Save turn
    nmj = result.new_messages_json()
    new_msgs = state.get("messages", [])
    if isinstance(nmj, (str, bytes)) and len(str(nmj).strip()) > 2:
        new_msgs = new_msgs + [nmj]
    return {
        "project_details": merged,
        "messages": new_msgs,
        "language": state.get("language", "English"),
        "class_profile": state.get("class_profile", ""),
        "session_id": state.get("session_id"),
    }


# get_standards node
async def get_standards(state: PBLState, writer) -> Dict[str, Any]:
    logger.debug("ENTERING get_standards…")

    # 1) Lang codes
    lang = state.get("language", "English")
    tgt = LANG_CODE_MAP.get(lang, "en")
    src = "en"

    # 2) Section header
    header = get_preset("get_standards_header", lang)
    writer(header)

    # 3) Build deps
    pd = state.get("project_details", {}) or {}
    deps = ProjectDetails(
        topic=pd.get("topic", ""),
        grade_level=pd.get("grade_level", "5"),
        duration_preference=pd.get("duration_preference", ""),
        age_range=pd.get("age_range"),
        content_area_focus=pd.get("content_area_focus"),
        learning_outcomes=pd.get("learning_outcomes", []),
        requires_experimentation=pd.get("requires_experimentation", False),
        involves_data_collection=pd.get("involves_data_collection", False),
        needs_mathematical_analysis=pd.get("needs_mathematical_analysis", False),
        includes_design_challenge=pd.get("includes_design_challenge", False),
        uses_technology_tools=pd.get("uses_technology_tools", False),
        community_connection_desired=pd.get("community_connection_desired", False),
        hands_on_emphasis=pd.get("hands_on_emphasis", False),
        research_intensive=pd.get("research_intensive", False),
        presentation_focused=pd.get("presentation_focused", False),
        collaborative_emphasis=pd.get("collaborative_emphasis", False),
        implicit_goals=pd.get("implicit_goals", []),
        standard_codes=pd.get("standard_codes", []),
    )

    prompt = (
        f"Find relevant educational standards for a {deps.grade_level}th-grade project "
        f"about {deps.topic}. Align them with the project’s characteristics "
        f"and {deps.duration_preference} duration."
    )

    try:
        # 4) Invoke agent
        result = await standards_agent.run(prompt, deps=deps)
        alignment: StandardsAlignment = result.output
        std_dict = alignment.model_dump()

        if not std_dict.get("standards"):
            raise ValueError("No standards returned")

        # 5) Recommended Standards
        rec = get_preset("recommended_standards", lang)
        writer(rec)
        for std in std_dict["standards"]:
            block = (
                f"- **{std['code']}** ({std['type'].upper()}, Grade {std['grade_level']}):\n"
                f"    {std['description']}\n"
                f"    • Bloom’s: {std['primary_bloom_level'].capitalize()}, "
                f"DOK: {std['dok_level'].replace('_',' ').capitalize()}\n"
            )
            writer(localize(block, src, tgt))

        # 6) Prerequisites
        if std_dict.get("prerequisites"):
            prefix = get_preset("prerequisites_prefix", lang)
            body = ", ".join(std_dict["prerequisites"]) + "\n"
            writer(prefix + localize(body, src, tgt))

        # 7) Cross-curricular
        if std_dict.get("cross_curricular_connections"):
            prefix = get_preset("cross_curricular_prefix", lang)
            body = ", ".join(std_dict["cross_curricular_connections"]) + "\n"
            writer(prefix + localize(body, src, tgt))

        return {"standards_result": std_dict}

    except Exception as e:
        logger.error(f"get_standards failed: {e}", exc_info=True)
        # fallback minimal alignment
        fallback = {
            "standards": [
                {
                    "code": "DEFAULT-001",
                    "type": "ngss",
                    "description": (
                        "Fallback alignment used due to an internal error during standards retrieval."
                    ),
                    "grade_level": deps.grade_level,
                    "is_valid": False,
                    "primary_bloom_level": "understand",
                    "dok_level": "recall",
                    "project_specific_vocabulary": [],
                }
            ],
            "prerequisites": [],
            "cross_curricular_connections": [],
            "alignment_confidence": 0.0,
            "validation_issues": [f"Error: {str(e)[:200]}"],
        }
        fallback_msg = get_preset("fallback_standards", lang)
        writer(fallback_msg)
        return {"standards_result": fallback}


# get_knowledge_graph node
async def get_knowledge_graph(state: PBLState, writer) -> Dict[str, Any]:
    # 1) Lang codes
    lang = state.get("language", "English")
    tgt = LANG_CODE_MAP.get(lang, "en")
    src = "en"

    # 2) Section header
    writer(get_preset("get_kg_header", lang))

    # 3) Rebuild alignment (fallback stub on error)
    try:
        alignment = StandardsAlignment(**state["standards_result"])
    except ValidationError:
        logger.error("StandardsAlignment validation failed", exc_info=True)
        first_grade = (state.get("standards_result", {}).get("standards", [{}])[0] or {}).get("grade_level", "")
        alignment = StandardsAlignment(
            standards=[{
                "code": "DEFAULT-001",
                "type": "ngss",
                "description": "Default stub alignment used due to validation error in standards.",
                "grade_level": first_grade,
                "is_valid": False,
                "primary_bloom_level": "understand",
                "dok_level": "recall",
                "project_specific_vocabulary": []
            }],
            prerequisites=[],
            cross_curricular_connections=[],
            alignment_confidence=0.0,
            validation_issues=["StandardsAlignment fallback used"]
        )

    # 4) Which standard we’re using
    primary = alignment.primary_standard or ContextualStandard(
        code="UNKNOWN",
        description="No description available for the primary standard.",
        grade_level=str(alignment.standards[0].grade_level if alignment.standards else ""),
        is_valid=False,
        project_specific_vocabulary=[]
    )
    writer(
        get_preset("kg_standard_prefix", lang)
        + localize(f"{primary.code} — {primary.description}", src, tgt)
        + "\n\n"
    )

    # 4) Class Profile
    pd = state.get("project_details", {}) or {}
    topic = pd.get("topic", "")

    logger.info(f"Project topic to the knowledge graph agent: {topic}")

    # 5) Build the prompt (always English internally)
    prompt = (
        f"Here is the standard to analyze:\n"
        f"  • Code       : {primary.code}\n"
        f"  • Description: {primary.description}\n"
        f"  • Grade level: {primary.grade_level}\n\n"
        "Now produce a complete KnowledgeGraphResult JSON with:\n"
        "1. standard_code & standard_description (copy verbatim)\n"
        "2. 3 project_topics (name+1–2 sentence description)\n"
        "3. 2 cross_subject_connections (subject→connection)\n"
        "4. 2 real_world_applications (application+details)\n"
        "5. 2 curriculum_resources (title+url)\n"
        "6. 3 pbl_integration_ideas\n"
        "7. relevance_confidence (0.0–1.0)\n"
        f"\n\n(Relate all insights to project topic: **{topic}**)\n\n"
    )

    # 6) Ask the agent (non-streamed), get raw + structured
    try:
        result = await kg_agent.run(prompt, deps=alignment)
        raw = (
            getattr(result, "response", None)
            or getattr(result, "text", None)
            or getattr(result, "llm_response", None)
            or ""
        )
        if raw:
            writer(localize(raw, src, tgt))
        kg: KnowledgeGraphResult = result.output
    except Exception as e:
        logger.error("KG agent error or parse failure: %s", e, exc_info=True)
        writer(get_preset("kg_fallback", lang))
        kg = KnowledgeGraphResult(
            standard_code=primary.code,
            standard_description=primary.description,
            project_topics=[{"name": "<no data>", "description": "<none>"}],
            cross_subject_connections=[{"subject": "<no data>", "connection": "<none>"}],
            real_world_applications=[{"application": "<no data>", "details": "<none>"}],
            curriculum_resources=[{"title": "<no data>", "url": ""}],
            pbl_integration_ideas=["(no implementation ideas)"],
            relevance_confidence=0.0,
        )

    # 7) Display the structured insights
    writer(get_preset("kg_insights_header", lang))

    # Project topics
    writer(get_preset("project_topics_header", lang))
    for t in kg.project_topics:
        line = f"• {t['name']}: {t['description']}"
        writer(localize(f"  {line}", src, tgt) + "\n")

    # Cross-subject connections
    writer(get_preset("cross_subjects_header", lang))
    for c in kg.cross_subject_connections:
        line = f"• {c['subject']} → {c['connection']}"
        writer(localize(f"  {line}", src, tgt) + "\n")

    # Real-world applications
    writer(get_preset("real_world_header", lang))
    for a in kg.real_world_applications:
        line = f"• {a['application']}: {a['details']}"
        writer(localize(f"  {line}", src, tgt) + "\n")

    # Curriculum resources
    writer(get_preset("resources_header", lang))
    for r in kg.curriculum_resources:
        title = localize(r["title"], src, tgt)
        writer(f"  • {title}: {r['url']}\n")

    # Implementation ideas
    writer(get_preset("implementation_header", lang))
    for idea in kg.pbl_integration_ideas:
        writer(localize(f"  • {idea}", src, tgt) + "\n")

    # Confidence
    writer(get_preset("confidence_prefix", lang) + f"{kg.relevance_confidence:.0%}\n")

    return {"knowledge_graph_result": kg.model_dump()}


# Final planning node
async def create_project_options(state: PBLState, writer) -> Dict[str, Any]:
    """
    Generate or select PBL project options, preserving language and class_profile
    and handling empty-model responses gracefully.
    """
    logger.debug("ENTER create_project_options")

    # ── localization setup ─────────────────────────────────────────────────────
    lang = state.get("language", "English")
    tgt = LANG_CODE_MAP.get(lang, "en")
    src = "en"

    # always return these on every branch
    base_return = {
        "language": lang,
        "class_profile": state.get("class_profile", ""),
        "session_id": state.get("session_id"),
    }

    prev = state.get("project_options", {}) or {}
    opts = prev.get("project_options")

    # pre-compute all your localized labels once
    option_label = get_preset("option_label", lang).strip()
    rationale_label = get_preset("rationale_label", lang).lstrip("• ").strip()
    driving_label = get_preset("driving_question_label", lang).lstrip("• ").strip()
    endprod_label = get_preset("end_product_label", lang).lstrip("• ").strip()
    skills_label = get_preset("key_skills_label", lang).lstrip("• ").strip()
    objectives_label = get_preset("learning_objectives_label", lang).lstrip("• ").strip()
    assess_label = get_preset("assessment_summary_label", lang).lstrip("• ").strip()
    # if you have more fields like differentiation_notes, template_id, etc. you can add:
    diff_label = "Differentiation notes"
    tpl_id_label = "Template id"
    tpl_name_label = "Template name"
    tpl_rat_label = "Template rationale"

    # ── PHASE 1: generate three options if none exist ─────────────────────────
    if not opts:
        writer(get_preset("creating_options_header", lang))
        context = ProjectDesignContext(
            project_profile=ProjectDetails(**state.get("project_details", {})),
            standards_alignment=StandardsAlignment(**state.get("standards_result", {})),
            kg_insights=KnowledgeGraphResult(**state.get("knowledge_graph_result", {})),
            class_profile=state.get("class_profile", "")
        )

        try:
            result = await design_options_agent.run(
                "Generate 3 distinct project options and name them 1, 2, 3. Ensuring they are adequate for the class profile, in particular the age of the students.",
                deps=context
            )
            raw = (
                getattr(result, "response", None)
                or getattr(result, "text", None)
                or getattr(result, "llm_response", None)
                or ""
            )
            if raw:
                writer(localize(raw, src, tgt))

            # Validate the output structure
            data: ProjectOptionsResult = result.output
            project_options = data.project_options if hasattr(data, "project_options") else []
            
            # Ensure we have valid project options
            if not project_options or len(project_options) == 0:
                raise ValueError("No project options were generated")
                
            merged = {**prev, **data.model_dump()}
        except Exception as e:
            logger.error("Error generating project options: %s", e, exc_info=True)
            writer(get_preset("fallback_options", lang))
            
            # Create fallback options with required fields
            fallback_options = [
                ProjectOption(
                    template_id=f"fallback_{i}",
                    template_name=f"Project Option {i+1}",
                    template_rationale="This is a fallback option due to an error in generation.",
                    title=f"Project Option {i+1}",
                    focus_approach="General approach",
                    driving_question="What is the main question for this project?",
                    end_product="Students will create a final product.",
                    key_skills=["Critical thinking", "Collaboration"],
                    learning_objectives=["Students will learn key concepts."],
                    assessment_summary="Assessment will be based on the final product."
                ) for i in range(3)
            ]
            
            merged = {**prev, "project_options": [opt.model_dump() for opt in fallback_options], "configuration_details": {}}

        writer(get_preset("project_options_header", lang))
        for idx, opt in enumerate(merged.get("project_options", []), start=1):
            if idx > 1:
                writer("\n---\n")
            writer(f"> **{option_label} {idx}:** {localize(opt['template_name'], src, tgt)}\n")
            writer(f"- **{rationale_label}:** {localize(opt['template_rationale'], src, tgt)}\n")
            writer(f"- **{driving_label}:** {localize(opt['driving_question'], src, tgt)}\n")
            writer(f"- **{endprod_label}:** {localize(opt['end_product'], src, tgt)}\n")
            writer(f"- **{skills_label}:** {localize(', '.join(opt['key_skills']) or '—', src, tgt)}\n")
            writer(f"- **{objectives_label}:** {localize(', '.join(opt['learning_objectives']) or '—', src, tgt)}\n")
            writer(f"- **{assess_label}:** {localize(opt['assessment_summary'], src, tgt)}\n")

        writer("\n")
        writer(get_preset("choice_prompt", lang) + "\n")
        return {**base_return, "project_options": merged}

    # ── PHASE 2: user picks one, now render **all** details with your localized labels
    if opts and not prev.get("selection_complete", False):
        # Check for structured input first (from Streamlit)
        user_input = state.get("user_input")
        choice = None
        
        # Handle structured input with selected_id
        if isinstance(user_input, dict) and "selected_id" in user_input:
            choice = user_input.get("selected_id")
            if isinstance(choice, int) and 1 <= choice <= len(opts):
                logger.info(f"Using structured selection: {choice}")
        
        # Fall back to text parsing if no structured input or invalid choice
        if choice is None:
            user_in = (str(user_input) if user_input is not None else "").lower()
            m = re.search(rf"\b([1-{len(opts)}])\b", user_in)
            if m:
                choice = int(m.group(1))
            else:
                ords = {
                    "first": 1, "second": 2, "third": 3,
                    "primera": 1, "segunda": 2, "tercera": 3
                }
                for w, num in ords.items():
                    if w in user_in:
                        choice = num
                        break

        if not choice or not (1 <= choice <= len(opts)):
            writer(get_preset("invalid_choice", lang).format(max=len(opts)) + "\n")
            return {**base_return, "project_options": prev}

        selected = ProjectOption(**opts[choice - 1])

        # Header + title
        writer(get_preset("full_details_header", lang) + "\n")
        writer(f"> **{option_label} {choice}:** {localize(selected.template_name, src, tgt)}\n\n")

        # Now explicit bullet list of each field
        writer(f"- **{rationale_label}:** {localize(selected.template_rationale, src, tgt)}\n")
        writer(f"- **{driving_label}:** {localize(selected.driving_question, src, tgt)}\n")
        writer(f"- **{endprod_label}:** {localize(selected.end_product, src, tgt)}\n")
        writer(f"- **{skills_label}:** {localize(', '.join(selected.key_skills) or '—', src, tgt)}\n")
        writer(f"- **{objectives_label}:** {localize(', '.join(selected.learning_objectives) or '—', src, tgt)}\n")
        writer(f"- **{assess_label}:** {localize(selected.assessment_summary, src, tgt)}\n")

        # any extra fields you want to show:
        if getattr(selected, "differentiation_notes", None):
            writer(f"- **{diff_label}:** {localize(selected.differentiation_notes, src, tgt)}\n")
        writer(f"- **{tpl_id_label}:** {selected.template_id}\n")
        writer(f"- **{tpl_name_label}:** {localize(selected.template_name, src, tgt)}\n")
        writer(f"- **{tpl_rat_label}:** {localize(selected.template_rationale, src, tgt)}\n")

        writer("\n---\n\n")
        writer(get_preset("project_ready", lang) + "\n")

        saved_id = await _save_selected_option_to_mongo(state, selected, choice - 1)
        if saved_id:
            writer(f"\nSaved your selection (id: {saved_id}).\n")

        updated = {
            **prev,
            "user_selected_option": choice - 1,
            "selection_complete": True,
            "saved_mongo_id": saved_id,  # handy in UI if needed
        }
        return {**base_return, "project_options": updated}

    # ── FALLBACK: nothing to do ────────────────────────────────────────────────
    return {**base_return, "project_options": prev}


async def _save_selected_option_to_mongo(state: PBLState, selected: ProjectOption, choice_index: int) -> Optional[str]:
    if _templates_col is None:
        logger.warning("Mongo not configured (ATLAS_URI missing) — skipping save.")
        return None

    try:
        doc = {
            "session_id": state.get("session_id"),
            "language": state.get("language", "English"),
            "class_profile": state.get("class_profile", ""),
            "project_details": state.get("project_details"),
            "standards_result": state.get("standards_result"),
            "knowledge_graph_result": state.get("knowledge_graph_result"),
            "selected_option_index": choice_index,
            "selected_option": selected.model_dump(),
            "all_options": (state.get("project_options", {}) or {}).get("project_options", []),
            "created_at": datetime.now(timezone.utc),
        }
        res = await _templates_col.insert_one(doc)
        return str(res.inserted_id)
    except Exception as e:
        logger.error("Failed to save selected option to MongoDB: %s", e, exc_info=True)
        return None


# Conditional edge function to determine next steps after info gathering
def route_after_info_gathering(state: PBLState):
    """If any of topic/grade/duration is missing, ask again; otherwise go to standards."""
    details = state.get("project_details", {}) or {}
    topic = str(details.get("topic") or "").strip()
    grade = str(details.get("grade_level") or "").strip()
    duration = str(details.get("duration_preference") or "").strip()
    print(f"DEBUG: topic='{topic}', grade='{grade}', duration='{duration}'")
    if not (topic and grade and duration):
        return "ask_for_details"
    return "get_standards"


# Interrupt the graph to get details of project
def ask_for_details(state: PBLState):
    value = interrupt({})
    return {
        "user_input": value,
        "language": state.get("language", "English"),
        "class_profile": state.get("class_profile", ""),
        "session_id": state.get("session_id"),
    }


# Interrupt the graph to get selected project
def ask_for_option(state: PBLState):
    value = interrupt({})
    return {
        "user_input": value,
        "language": state.get("language", "English"),
        "class_profile": state.get("class_profile", ""),
        "session_id": state.get("session_id"),
    }


def route_after_project_options(state: PBLState):
    """If selection_complete=True → END, else ask user again for the choice."""
    opts = state.get("project_options", {}) or {}
    if opts.get("selection_complete"):
        return END
    return "ask_for_option"


# Build the graph
def build_pbl_agent_graph():
    graph = StateGraph(PBLState)

    # 1) Register all nodes
    graph.add_node("gather_info", gather_info)
    graph.add_node("ask_for_details", ask_for_details)
    graph.add_node("ask_for_option", ask_for_option)
    graph.add_node("get_standards", get_standards)
    graph.add_node("get_knowledge_graph", get_knowledge_graph)
    graph.add_node("create_project_options", create_project_options)

    # 2) Start → gather_info
    graph.add_edge(START, "gather_info")

    # 3) After gather_info:
    #    • Missing slots → ask_for_details
    #    • All slots present → get_standards
    graph.add_conditional_edges(
        "gather_info",
        route_after_info_gathering,
        ["ask_for_details", "get_standards"]
    )
    graph.add_edge("ask_for_details", "gather_info")

    # 4) Once slots filled → standards → KG → options
    graph.add_edge("get_standards", "get_knowledge_graph")
    graph.add_edge("get_knowledge_graph", "create_project_options")

    # 5) Inside create_project_options:
    #    • If selection_complete=False → ask_for_option (to get the user's choice)
    #    • If selection_complete=True  → END
    graph.add_conditional_edges(
        "create_project_options",
        route_after_project_options,
        ["ask_for_option", END]
    )
    graph.add_edge("ask_for_option", "create_project_options")

    return graph.compile(checkpointer=MemorySaver())


# Create the PBL agent graph
pbl_agent_graph = build_pbl_agent_graph()


# Function to run the PBL agent
async def run_pbl_agent(user_input: str, thread_id: str = None, class_profile: str = "", language: str = "English"):
    """Run the pbl agent with the given user input.

    Args:
        user_input: The user's project description or requirements
        thread_id: Optional thread ID for conversation tracking. If not provided, a new one will be generated.
    """
    import uuid
    from langgraph.types import Command

    # Generate a thread ID if not provided
    if thread_id is None:
        thread_id = str(uuid.uuid4())

    # Prepare the config with thread_id
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    # Initialize the state with user input
    initial_state = {
        "user_input": user_input,
        "class_profile": class_profile,
        "language": language,
        "project_details": {},
        "standards_result": {
            "standards": [
                {
                    "code": "INIT",
                    "type": "other",
                    "description": "Initializing",
                    "grade_level": "",
                    "is_valid": False,
                    "primary_bloom_level": "understand",
                    "dok_level": "recall",
                    "project_specific_vocabulary": []
                }
            ],
            "prerequisites": [],
            "cross_curricular_connections": [],
            "alignment_confidence": 0.0,
            "validation_issues": []
        },
        "knowledge_graph_result": {
            "standard_code": "",
            "standard_description": "",
            "project_topics": [],
            "cross_subject_connections": [],
            "real_world_applications": [],
            "curriculum_resources": [],
            "pbl_integration_ideas": [],
            "relevance_confidence": 0.0
        },
        "project_options": {
            "user_selected_option": None,
            "selection_complete": False,
            "response": "",
            "selected_template": "",
            "template_rationale": "",
            "project_options": [],
            "configuration_details": {}
        },
        "messages": []
    }

    # Check if this is the first message or a continuation
    if not hasattr(run_pbl_agent, 'chat_history'):
        run_pbl_agent.chat_history = []

    # Run the PBL agent graph with the config
    try:

        if len(run_pbl_agent.chat_history) == 0:
            result = await pbl_agent_graph.ainvoke(initial_state, config=config)
        else:
            result = await pbl_agent_graph.ainvoke(
                Command(resume=user_input),
                config=config
            )

        print(f"\n=== Graph Execution Complete ===")
        print(f"Result keys: {list(result.keys())}")
        if 'project_options' in result:
            print(f"Project options type: {type(result['project_options'])}")
            print(f"Project options content: {result['project_options']}")

    except Exception as e:
        print(f"\n!!! Error in pbl_agent_graph.ainvoke: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

    # Update chat history
    run_pbl_agent.chat_history.append({"role": "user", "content": user_input})
    if "project_options" in result:
        run_pbl_agent.chat_history.append({"role": "assistant", "content": str(result["project_options"])})

    # Return the final plan
    return result.get("project_options", {})


async def main():
    # Example user input
    user_input = "I want to plan a 2 week project about the solar system for grade 5. My class size is 20 we have access only to tablets."

    try:
        # Run the PBL agent with a sample thread ID for testing
        project_options = await run_pbl_agent(
            user_input=user_input,
            thread_id="test_thread_123"  # Fixed thread ID for testing
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
