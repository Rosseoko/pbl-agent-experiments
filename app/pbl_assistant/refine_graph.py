# app/pbl_assistant/refine_graph.py

from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from typing_extensions import Annotated, NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from pydantic_ai.exceptions import ToolRetryError, UnexpectedModelBehavior
from pydantic import ValidationError
import certifi

# Get certifi CA bundle path
CA = certifi.where()


# Mongo (optional)
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from bson import ObjectId
except Exception as e:
    AsyncIOMotorClient = None  # type: ignore
    ObjectId = None  # type: ignore
    logging.getLogger(__name__).warning("Mongo not available for refine graph: %s", e)

# Models & localization
from pydantic import ValidationError
from app.pbl_assistant.models.profiling import (
    ProjectOption,
    StandardsAlignment,
    KnowledgeGraphResult,
)
from app.pbl_assistant.localization import LANG_CODE_MAP, localize, get_preset

# Agent
from app.pbl_assistant.agents.refining_agent import (
    refining_agent,
    RefinementContext,
    RefinementResult,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - refine_graph - %(levelname)s - %(message)s",
)

# ──────────────────────────────────────────────────────────────────────────────
# Mongo init (same DB/collection as generation flow)
# ──────────────────────────────────────────────────────────────────────────────
ATLAS_URI = os.getenv("ATLAS_URI", "mongodb+srv://erandDevbd:oPDTDscngZ6geaAX@cluster0-ea24.kwhgj0v.mongodb.net/")
ATLAS_DB = os.getenv("ATLAS_DB", "erandiapp")

_mongo_client = None
_mongo_db = None
_templates_col = None

if AsyncIOMotorClient and ATLAS_URI:
    try:
        _mongo_client = AsyncIOMotorClient(
            ATLAS_URI,
            tlsCAFile=CA,
            connectTimeoutMS=20000,
            serverSelectionTimeoutMS=20000,
        )
        _mongo_db = _mongo_client[ATLAS_DB]
        _templates_col = _mongo_db["project_templates"]
        logger.info("Refine graph: MongoDB connected")
    except Exception as e:
        logger.warning("Refine graph: Mongo init failed: %s", e)

# ──────────────────────────────────────────────────────────────────────────────
# State
# ──────────────────────────────────────────────────────────────────────────────
class RefineState(TypedDict, total=False):
    # Inputs
    change_request: str
    selected_option: Dict[str, Any] | ProjectOption
    standards_result: Dict[str, Any] | StandardsAlignment | None
    knowledge_graph_result: Dict[str, Any] | KnowledgeGraphResult | None
    language: NotRequired[str]
    class_profile: NotRequired[str]
    session_id: Optional[str]
    source_doc_id: Optional[str]
    strict: NotRequired[bool]
    idempotency_key: Optional[str]

    # Conversation memory (optional, to align with your other graphs)
    messages: Annotated[List[bytes], lambda x, y: x + y]

    # Outputs
    refine_result: Dict[str, Any]
    saved_mongo_id: Optional[str]


# ──────────────────────────────────────────────────────────────────────────────
# Nodes
# ──────────────────────────────────────────────────────────────────────────────
async def refine_project(state: RefineState, writer) -> Dict[str, Any]:
    """
    Apply a teacher's natural-language change request to a selected ProjectOption,
    performing a full rewrite with dependency-aware updates via `refining_agent`.
    If the model fails to return a valid update, perform a second-pass run and,
    as a last resort, a deterministic fallback patch for the targeted field(s).
    """
    lang = state.get("language", "English")
    tgt = LANG_CODE_MAP.get(lang, "en")
    src = "en"

    # Basic validation
    req = (state.get("change_request") or "").strip()
    if not req:
        msg = get_preset("refine_error_missing_request", lang) if callable(get_preset) else "Please provide a change request."
        writer(localize(msg, src, tgt))
        return {
            "refine_result": {
                "change_summary": "No change performed (missing request).",
                "affected_fields": [],
                "warnings": ["missing_change_request"],
                "updated_project": state.get("selected_option") or {},
            }
        }

    # Build current project model
    try:
        current_project = (
            ProjectOption(**state["selected_option"])
            if isinstance(state.get("selected_option"), dict)
            else state["selected_option"]
        )
        if current_project is None:
            raise ValueError("No selected_option provided.")
    except Exception as e:
        logger.error("Invalid selected_option: %s", e, exc_info=True)
        writer("Could not parse the selected project to refine.\n")
        return {
            "refine_result": {
                "change_summary": "No change performed (invalid selected project).",
                "affected_fields": [],
                "warnings": ["invalid_selected_option"],
                "updated_project": state.get("selected_option") or {},
            }
        }

    # Optional deps
    stds = state.get("standards_result")
    kg = state.get("knowledge_graph_result")

    try:
        stds_model: StandardsAlignment | None = None
        if stds:
            stds_model = StandardsAlignment(**stds) if isinstance(stds, dict) else stds
    except ValidationError:
        logger.warning("StandardsAlignment validation failed; ignoring standards for refinement")
        stds_model = None

    try:
        kg_model: KnowledgeGraphResult | None = None
        if kg:
            kg_model = KnowledgeGraphResult(**kg) if isinstance(kg, dict) else kg
    except ValidationError:
        logger.warning("KnowledgeGraphResult validation failed; ignoring KG for refinement")
        kg_model = None

    deps = RefinementContext(
        current_project=current_project,
        language=lang,
        class_profile=state.get("class_profile"),
        standards_alignment=stds_model,
        knowledge_graph_result=kg_model,
        strict=bool(state.get("strict", False)),
    )

    # Helpers
    def _diff_fields(a: ProjectOption, b: ProjectOption) -> list[str]:
        watch = [
            "title","focus_approach","driving_question","end_product",
            "key_skills","learning_objectives","key_activities",
            "assessment_highlights","assessment_summary",
            "template_name","template_rationale","differentiation_notes",
        ]
        return [k for k in watch if getattr(a, k, None) != getattr(b, k, None)]

    def _fallback_patch(req_text: str, proj: ProjectOption) -> tuple[ProjectOption, list[str], list[str], str]:
        """Minimal deterministic patch if LLM fails. For now, handle driving_question focus requests."""
        rq = req_text.lower()
        warnings: list[str] = ["llm_fallback_patch_applied"]
        affected: list[str] = []

        new_proj = proj.model_copy(deep=True)

        # Heuristic: user mentions driving question
        if any(k in rq for k in ["driving question", "driving_question", "dq"]):
            # Try to extract a focus phrase; if we see 'pollinator' or 'mexico city', craft a good DQ.
            focus_dq = None
            if "pollinator" in rq and ("mexico city" in rq or "cdmx" in rq):
                focus_dq = "How can we investigate and protect pollinators in Mexico City through observation, data, and design?"
            elif "pollinator" in rq:
                focus_dq = "How can we investigate and protect local pollinators through observation, data, and design?"
            elif "mexico city" in rq or "cdmx" in rq:
                focus_dq = "How can we investigate and explain urban biodiversity in Mexico City using models, data, and community research?"
            # Generic fallback
            if not focus_dq:
                focus_dq = f"How can we refine our project to address: {req_text.strip()}?"

            if new_proj.driving_question != focus_dq:
                new_proj.driving_question = focus_dq
                affected.append("driving_question")

            # Optional light ripple: align end_product wording if it references old focus
            if "pollinator" in focus_dq.lower():
                if new_proj.end_product:
                    if "pollinator" not in (new_proj.end_product or "").lower():
                        new_proj.end_product = (
                            "An interactive exhibit that presents student-built models, "
                            "data visualizations, and explanations about urban pollinators in Mexico City."
                        )
                        affected.append("end_product")
                if isinstance(new_proj.key_activities, list):
                    if not any("pollinator" in (a or "").lower() for a in new_proj.key_activities):
                        new_proj.key_activities = list(new_proj.key_activities or []) + [
                            "Conduct transect counts of urban pollinators and map hotspots near the school",
                            "Build and test simple pollinator-friendly planters or bee hotels; track visits"
                        ]
                        affected.append("key_activities")
                if isinstance(new_proj.learning_objectives, list):
                    if not any("pollinator" in (a or "").lower() for a in new_proj.learning_objectives):
                        new_proj.learning_objectives = list(new_proj.learning_objectives or []) + [
                            "Use observational data to explain pollinator presence and patterns in urban settings",
                        ]
                        affected.append("learning_objectives")

        change_summary = f"Applied deterministic fallback patch based on request: {req_text}"
        if not affected:
            warnings.append("no_change_detected")
        return new_proj, affected, warnings, change_summary

    # Run agent (streaming with partial tolerance)
    try:
        last_good: RefinementResult | None = None

        async with refining_agent.run_stream(req, deps=deps) as result:
            async for msg, last in result.stream_structured(debounce_by=0.01):
                try:
                    parsed = await result.validate_structured_result(msg, allow_partial=True)
                    if parsed:
                        last_good = parsed
                except (ValidationError, ToolRetryError, UnexpectedModelBehavior):
                    continue

            try:
                out: RefinementResult | None = await result.get_data()
            except UnexpectedModelBehavior:
                out = None

            if out is None:
                out = last_good

        # Extract or coerce
        updated_proj = getattr(out, "updated_project", None) if out else None
        if not isinstance(updated_proj, ProjectOption):
            updated_proj = current_project

        change_summary = (getattr(out, "change_summary", None) or "").strip() if out else ""
        affected_fields = list(getattr(out, "affected_fields", []) or []) if out else []
        warnings = list(getattr(out, "warnings", []) or []) if out else []

        # If nothing changed, try a **second pass** with a firmer instruction
        if updated_proj == current_project:
            try:
                force_suffix = (
                    "\n\nReturn ONLY a valid RefinementResult JSON conforming exactly to the schema. "
                    "You MUST update the requested fields. Do not omit required fields."
                )
                result2 = await refining_agent.run(req + force_suffix, deps=deps)
                out2: RefinementResult = result2.output
                if out2 and out2.updated_project:
                    updated_proj = out2.updated_project
                    change_summary = out2.change_summary or change_summary
                    affected_fields = out2.affected_fields or affected_fields
                    warnings = out2.warnings or warnings
            except Exception as e:
                logger.warning("Second-pass refine failed: %s", e)

        # If still unchanged, apply **deterministic fallback patch**
        if updated_proj == current_project:
            patched, affected2, warnings2, cs2 = _fallback_patch(req, current_project)
            updated_proj = patched
            # Merge effects smartly
            if cs2 and not change_summary:
                change_summary = cs2
            affected_fields = list(set((affected_fields or []) + affected2))
            warnings = list(set((warnings or []) + warnings2))

        # If we still somehow have no summary, synthesize one
        if not change_summary:
            change_summary = f"Applied teacher request: {req}"

        # If still no affected_fields, compute diff
        if not affected_fields:
            affected_fields = _diff_fields(current_project, updated_proj)
            if not affected_fields and "no_change_detected" not in warnings:
                warnings.append("no_change_detected")

        # Stream confirmation
        writer(localize("✅ Changes applied:\n", src, tgt))
        writer(localize(f"{change_summary}\n", src, tgt))
        if affected_fields:
            writer(localize(f"Affected fields: {', '.join(affected_fields)}\n", src, tgt))
        if warnings:
            writer(localize(f"Warnings: {', '.join(warnings)}\n", src, tgt))

        result_dict = {
            "updated_project": updated_proj.model_dump(),
            "change_summary": change_summary,
            "affected_fields": affected_fields,
            "warnings": warnings,
        }

        return {
            "refine_result": result_dict,
            "selected_option": updated_proj.model_dump(),
            "language": lang,
            "class_profile": state.get("class_profile", ""),
            "session_id": state.get("session_id"),
            "source_doc_id": state.get("source_doc_id"),
            "idempotency_key": state.get("idempotency_key"),
        }

    except Exception as e:
        logger.error("Refining agent failed: %s", e, exc_info=True)
        writer(localize("We couldn't apply the requested change due to an internal error.\n", src, tgt))
        return {
            "refine_result": {
                "change_summary": "No change performed (agent error).",
                "affected_fields": [],
                "warnings": ["refining_agent_error"],
                "updated_project": current_project.model_dump(),
            }
        }


async def save_version(state: RefineState, writer) -> Dict[str, Any]:
    """
    Persist a new version of the project to MongoDB with parent/root/version.
    If Mongo is not configured, skip saving gracefully.
    """
    if _templates_col is None or not ObjectId:
        logger.warning("Mongo not configured for refinement save — skipping persistence.")
        return {"saved_mongo_id": None}

    source_doc_id = state.get("source_doc_id")
    if not source_doc_id:
        logger.info("No source_doc_id provided; saving as a standalone document.")
        parent_doc = None
    else:
        try:
            parent_doc = await _templates_col.find_one({"_id": ObjectId(source_doc_id)})
        except Exception as e:
            logger.warning("Failed to load parent doc %s: %s", source_doc_id, e)
            parent_doc = None

    # Compute versioning
    root_id = None
    version = 1
    if parent_doc:
        root_id = parent_doc.get("root_id") or parent_doc.get("_id")
        version = int(parent_doc.get("version", 1)) + 1

    # Idempotency (optional)
    idem = state.get("idempotency_key")
    if idem and parent_doc:
        existing = await _templates_col.find_one({
            "parent_id": parent_doc["_id"],
            "idempotency_key": idem,
        })
        if existing:
            saved_id = str(existing["_id"])
            writer(f"(Idempotent) Using previously saved refinement: {saved_id}\n")
            return {"saved_mongo_id": saved_id}

    # Prepare doc
    refine_result = state.get("refine_result", {}) or {}
    updated_project = (
        refine_result.get("updated_project")
        or state.get("selected_option")
        or {}
    )

    doc = {
        "session_id": state.get("session_id"),
        "language": state.get("language", "English"),
        "class_profile": state.get("class_profile", ""),
        # carry forward original context if available
        "project_details": parent_doc.get("project_details") if parent_doc else None,
        "standards_result": state.get("standards_result") or (parent_doc.get("standards_result") if parent_doc else None),
        "knowledge_graph_result": state.get("knowledge_graph_result") or (parent_doc.get("knowledge_graph_result") if parent_doc else None),
        # versioning
        "refinement": True,
        "parent_id": parent_doc["_id"] if parent_doc else None,
        "root_id": root_id,
        "version": version,
        "idempotency_key": idem,
        # payload
        "selected_option": updated_project,
        "selected_option_index": parent_doc.get("selected_option_index") if parent_doc else None,
        "all_options": parent_doc.get("all_options") if parent_doc else None,
        # audit
        "change_request": state.get("change_request"),
        "affected_fields": refine_result.get("affected_fields", []),
        "warnings": refine_result.get("warnings", []),
        "created_at": datetime.now(timezone.utc),
    }

    try:
        res = await _templates_col.insert_one(doc)
        saved_id = str(res.inserted_id)
        writer(f"Saved refined project (id: {saved_id}).\n")
        return {"saved_mongo_id": saved_id}
    except Exception as e:
        logger.error("Failed saving refined version: %s", e, exc_info=True)
        writer("Could not save the refined version to the database.\n")
        return {"saved_mongo_id": None}


# ──────────────────────────────────────────────────────────────────────────────
# Graph builder
# ──────────────────────────────────────────────────────────────────────────────
def build_refine_graph():
    graph = StateGraph(RefineState)
    graph.add_node("refine_project", refine_project)
    graph.add_node("save_version", save_version)

    graph.add_edge(START, "refine_project")
    graph.add_edge("refine_project", "save_version")
    graph.add_edge("save_version", END)

    return graph.compile(checkpointer=MemorySaver())


pbl_refine_graph = build_refine_graph()

# ──────────────────────────────────────────────────────────────────────────────
# Convenience entry point for backend callers (e.g., Streamlit)
# ──────────────────────────────────────────────────────────────────────────────
async def refine_project_option(
    *,
    source_doc_id: Optional[str],
    change_request: str,
    session_id: Optional[str] = None,
    language: str = "English",
    class_profile: str = "",
    standards_result: Dict[str, Any] | None = None,
    knowledge_graph_result: Dict[str, Any] | None = None,
    selected_option: Dict[str, Any] | None = None,
    strict: bool = False,
    idempotency_key: Optional[str] = None,
    thread_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Load the source document (if provided), run the refine graph, and return:
      { "updated_doc_id": str | None, "refine_result": {...}, "updated_project": {...} }
    If `selected_option` is provided, it overrides the one loaded from Mongo.
    """
    # If no selected_option provided, try to load it from Mongo
    if selected_option is None and _templates_col and source_doc_id and ObjectId:
        try:
            parent = await _templates_col.find_one({"_id": ObjectId(source_doc_id)})
            if parent and "selected_option" in parent:
                selected_option = parent["selected_option"]
                # default standards/KG from parent if not explicitly passed
                standards_result = standards_result or parent.get("standards_result")
                knowledge_graph_result = knowledge_graph_result or parent.get("knowledge_graph_result")
                session_id = session_id or parent.get("session_id")
                language = language or parent.get("language", "English")
                class_profile = class_profile or parent.get("class_profile", "")
        except Exception as e:
            logger.warning("Could not load parent doc %s: %s", source_doc_id, e)

    initial_state: RefineState = {
        "change_request": change_request,
        "selected_option": selected_option or {},
        "standards_result": standards_result,
        "knowledge_graph_result": knowledge_graph_result,
        "language": language,
        "class_profile": class_profile,
        "session_id": session_id,
        "source_doc_id": source_doc_id,
        "strict": strict,
        "idempotency_key": idempotency_key,
        "messages": [],
    }

    config = {"configurable": {"thread_id": thread_id or "refine_" + datetime.utcnow().isoformat()}}
    result = await pbl_refine_graph.ainvoke(initial_state, config=config)

    refine_result = result.get("refine_result") or {}
    updated_project = (
        refine_result.get("updated_project") or result.get("selected_option") or selected_option or {}
    )
    return {
        "updated_doc_id": result.get("saved_mongo_id"),
        "refine_result": refine_result,
        "updated_project": updated_project,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Local quick test (optional)
# ──────────────────────────────────────────────────────────────────────────────
async def _demo():
    fake_option = {
        "template_id": "scientific_inquiry",
        "template_name": "Scientific Inquiry Project",
        "template_rationale": "Inquiry approach engages students in space exploration through experiments.",
        "title": "Junior Astronomers",
        "focus_approach": "Modeling key aspects of astronomy to explain celestial phenomena.",
        "driving_question": "How can we investigate brightness and motion in the solar system?",
        "end_product": "Interactive exhibit with models and data findings.",
        "key_skills": ["Analyzing data", "Using models", "Explanations"],
        "learning_objectives": ["Explain brightness", "Model sun/moon cycles"],
        "key_activities": ["Test light sources", "Build scale models"],
        "assessment_highlights": ["Models of motions", "Pattern analysis"],
        "assessment_summary": "Evaluate investigations, data quality, models, and explanations.",
        "differentiation_notes": "Concrete materials; flexible outputs.",
    }
    out = await refine_project_option(
        source_doc_id=None,
        change_request="Make the driving question focus on Mars exploration and add a telescope-building activity.",
        selected_option=fake_option,
        language="English",
        class_profile="Grade 5, mixed reading levels.",
    )
    print(out)

if __name__ == "__main__":
    try:
        asyncio.run(_demo())
    except RuntimeError:
        # When running inside environments with a running loop
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(_demo())
