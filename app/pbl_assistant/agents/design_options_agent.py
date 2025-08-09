from pydantic_ai import Agent, RunContext
from pydantic_ai.models.bedrock import BedrockConverseModel
from typing import List, Dict, Any, Optional
import os
import importlib
import logging
from app.pbl_assistant.aws_config import get_bedrock_client

# Import models
# Import from the main designing package which exposes all necessary components
from app.pbl_assistant.models.designing import (
    BaseTemplate, Duration, SocialStructure, CognitiveComplexity,
    AuthenticityLevel, ScaffoldingIntensity, ProductComplexity, DeliveryMode
)
from app.pbl_assistant.models.designing.configuration.dimensional_config import DimensionalConfiguration
from app.pbl_assistant.models.designing.configuration.configured_project import ConfiguredProject
from app.pbl_assistant.models.profiling import ProjectDesignContext, ProjectOptionsResult, ProjectOption, ProjectDetails, StandardsAlignment, KnowledgeGraphResult
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# Agent Definition
design_options_agent = Agent(
    model=BedrockConverseModel(
        "anthropic.claude-3-sonnet-20240229-v1:0",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    ),
    deps_type=ProjectDesignContext,
    result_type=ProjectOptionsResult,
    result_retries=2,
    system_prompt="""
Your name is Erandi, you are an energetic and friendly expert PBL designer. You receive a ProjectDesignContext containing:
  • project_profile: teacher’s project details  
  • standards_alignment: aligned educational standards  
  • kg_insights: knowledge-graph connections  

PHASE 1 – MULTI-TEMPLATE OPTION GENERATION
1. Call the `get_available_templates()` tool to retrieve the full catalog of templates.
2. For each template in that catalog, call the `evaluate_template_fit(template_id, template_info)` tool to score how well it fits the project context.
3. **Select three different templates** (no repeats).  
4. For each of the three options, produce a JSON object with these fields:
   • `template_id`: the catalog key (e.g. `"engineering_design"`)  
   • `template_name`: the human-readable display name (e.g. `"Engineering Design Challenge"`)  
   • `template_rationale`: one sentence explaining why this template fits _this_ option  
   • `title`             : the title of the option
   • `focus_approach`    : the focus approach of the option
   • `key_activities`         : the key activities of the option
   • `assessment_highlights`  : the assessment highlights of the option
   • `differentiation_notes`  : the differentiation notes of the option
   • `driving_question`: a clear, open‐ended question driving student inquiry  
   • `end_product`: what students will create or deliver  
   • `key_skills`: a list of 3–5 skills students will practice  
   • `learning_objectives`: a list of objectives, each tied explicitly to one of the aligned standards  
   • `assessment_summary`: a concise description of how you will assess student work  

PHASE 2 – USER SELECTION
1. If options already exist, list them exactly as:
     1. Option 1 title  
     2. Option 2 title  
     3. Option 3 title  
2. Prompt the teacher: “Por favor elige 1, 2 o 3.”  
3. Validate the choice; if invalid, ask again; if valid, set `user_selected_option` to 0, 1, or 2.

Return a fully populated `ProjectOptionsResult` with:
  • `project_options`: an array of the three option objects  
  • `configuration_details`: (you can leave empty if unused)  
  • `user_selected_option`, `selection_complete`, and `response` as per the spec.
""",
)


# — Inject structured PBL context into every run —
@design_options_agent.system_prompt
async def add_project_context(ctx: RunContext[ProjectDesignContext]) -> str:
    p: ProjectDetails       = ctx.deps.project_profile
    s: StandardsAlignment   = ctx.deps.standards_alignment
    k: KnowledgeGraphResult = ctx.deps.kg_insights
    cp = ctx.deps.class_profile

    # Profile characteristics
    chars = []
    if p.hands_on_emphasis:          chars.append("hands-on")
    if p.community_connection_desired: chars.append("community")
    if p.research_intensive:         chars.append("research")
    if p.includes_design_challenge:  chars.append("design-challenge")
    if p.requires_experimentation:    chars.append("experimentation")
    if p.collaborative_emphasis:     chars.append("collaboration")
    chars_txt = ", ".join(chars) or "general"

    # Standards summary
    std_lines = []
    for std in s.standards:
        desc = std.description if len(std.description) < 80 else std.description[:77] + "…"
        std_lines.append(f"- {std.code} ({std.grade_level}): {desc}")
    standards_txt = "\n".join(std_lines)

    # KG highlights
    topics = ", ".join([t.get("name","N/A") for t in k.project_topics[:3]])
    xs     = ", ".join([f"{c.get('subject')}→{c.get('connection')}" for c in k.cross_subject_connections[:2]])
    apps   = ", ".join([a.get("application","") for a in k.real_world_applications[:2]])

    return f"""
PROJECT CONTEXT
• Topic         : {p.topic}
• Grade level   : {p.grade_level}
• Duration      : {p.duration_preference}
• Characteristics: {chars_txt}

STANDARDS ALIGNMENT ({len(s.standards)}):
{standards_txt}

KG INSIGHTS
• Project topics           : {topics}
• Cross-subject connections: {xs}
• Real-world applications   : {apps}

Use all of the above to pick the best template and then generate
3 fully fleshed-out project options ensuring they are adequate for the class profile, in particular the age of the students.

Adapt all the proposed options to the class profile, consider its limitations and capabilities:
{cp}

"""


@design_options_agent.tool
async def get_available_templates(ctx: RunContext[ProjectDesignContext]) -> Dict[str, Dict[str, Any]]:
    """Get available templates with their key characteristics"""
    
    # Hardcoded template catalog for simplicity (KISS principle)
    # In production, this could scan directories dynamically
    templates = {
        "community_action": {
            "display_name": "Community Action Project",
            "description": "Students identify local issues, research root causes, and develop actionable solutions with community stakeholders",
            "strengths": ["civic_engagement", "research", "stakeholder_collaboration", "public_presentation"],
            "subject_areas": ["social_studies", "english_language_arts", "civics"],
            "complexity": "high",
            "community_engagement": "high"
        },
        "creative_expression": {
            "display_name": "Creative Expression Project",
            "description": "Students explore ideas through art and creative work shared with authentic audiences",
            "strengths": ["artistic_creation", "self_expression", "reflection", "presentation"],
            "subject_areas": ["arts", "english_language_arts"],
            "complexity": "low",
            "community_engagement": "medium"
        },
        "service_learning": {
            "display_name": "Service Learning Project",
            "description": "Students engage in hands-on service activities while developing empathy and teamwork skills",
            "strengths": ["hands_on", "empathy", "teamwork", "reflection"],
            "subject_areas": ["social_studies", "character_education"],
            "complexity": "low", 
            "community_engagement": "medium"
        },
        "technology_focused": {
            "display_name": "Technology Focused Project",
            "description": "Students explore coding and technology through creating simple digital projects",
            "strengths": ["coding", "digital_creation", "problem_solving", "presentation"],
            "subject_areas": ["technology", "computer_science"],
            "complexity": "medium",
            "community_engagement": "low"
        },
        "engineering_design": {
            "display_name": "Engineering Design Challenge",
            "description": "Students identify problems and design, build, and test solutions through iterative prototyping",
            "strengths": ["design_thinking", "hands_on", "prototyping", "iteration"],
            "subject_areas": ["science", "engineering", "mathematics"],
            "complexity": "high",
            "community_engagement": "medium"
        },
        "historical_inquiry": {
            "display_name": "Historical Investigation",
            "description": "Students investigate historical questions using primary sources and historical thinking skills",
            "strengths": ["research", "analysis", "historical_thinking", "writing"],
            "subject_areas": ["social_studies", "history"],
            "complexity": "medium",
            "community_engagement": "low"
        },
        "mathematical_modeling": {
            "display_name": "Mathematical Modeling",
            "description": "Students apply mathematical concepts to model and analyze real-world situations",
            "strengths": ["problem_solving", "data_analysis", "modeling", "mathematical_thinking"],
            "subject_areas": ["mathematics"],
            "complexity": "high",
            "community_engagement": "low"
        },
        "research_investigation": {
            "display_name": "Research Investigation",
            "description": "Students conduct in-depth research on academic topics using scholarly sources",
            "strengths": ["research", "critical_analysis", "academic_writing", "presentation"],
            "subject_areas": ["english_language_arts", "social_studies", "science"],
            "complexity": "high",
            "community_engagement": "low"
        },
        "scientific_inquiry": {
            "display_name": "Scientific Inquiry Project",
            "description": "Students design and conduct scientific investigations following the scientific method",
            "strengths": ["experimentation", "data_analysis", "scientific_method", "research"],
            "subject_areas": ["science", "mathematics"],
            "complexity": "medium",
            "community_engagement": "low"
        },
        "debate_argumentation": {
            "display_name": "Debate & Argumentation",
            "description": "Students research controversial topics and develop structured arguments with evidence",
            "strengths": ["research", "argumentation", "public_speaking", "critical_thinking"],
            "subject_areas": ["english_language_arts", "social_studies"],
            "complexity": "medium",
            "community_engagement": "low"
        },
        "design_thinking": {
            "display_name": "Design Thinking Project",
            "description": "Students apply design thinking process to create human-centered solutions",
            "strengths": ["empathy", "ideation", "prototyping", "user_testing"],
            "subject_areas": ["technology", "arts", "engineering"],
            "complexity": "medium",
            "community_engagement": "medium"
        },
        "interdisciplinary": {
            "display_name": "Interdisciplinary Integration",
            "description": "Students explore complex topics through multiple subject lenses and connections",
            "strengths": ["cross_curricular", "systems_thinking", "synthesis", "integration"],
            "subject_areas": ["multiple"],
            "complexity": "high",
            "community_engagement": "medium"
        },
        "skill_application": {
            "display_name": "Skill Application Project",
            "description": "Students practice and demonstrate mastery of specific academic or technical skills",
            "strengths": ["skill_mastery", "practice", "demonstration", "feedback"],
            "subject_areas": ["career_technical", "mathematics", "language_arts"],
            "complexity": "low",
            "community_engagement": "low"
        },

    }
    
    return templates

@design_options_agent.tool
async def evaluate_template_fit(
    ctx: RunContext[ProjectDesignContext], 
    template_id: str, 
    template_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluate how well a template matches the project context"""
    
    profile = ctx.deps.project_profile
    
    score = 0
    reasons = []
    
    # Match project characteristics to template strengths
    template_strengths = template_info.get("strengths", [])
    
    if profile.community_connection_desired and "community_connection" in template_strengths:
        score += 3
        reasons.append("Strong community engagement match")
    
    if profile.hands_on_emphasis and "hands_on" in template_strengths:
        score += 2
        reasons.append("Hands-on activity alignment")
    
    if profile.research_intensive and "research" in template_strengths:
        score += 2
        reasons.append("Research focus alignment")
    
    if profile.includes_design_challenge and "design_challenge" in template_strengths:
        score += 3
        reasons.append("Design challenge perfect match")
        
    if profile.requires_experimentation and "experimentation" in template_strengths:
        score += 3
        reasons.append("Experimentation requirement match")
    
    if profile.collaborative_emphasis and "collaboration" in template_strengths:
        score += 1
        reasons.append("Collaboration support")

    if profile.iterative_emphasis and "iteration" in template_strengths:
        score += 1
        reasons.append("Iteration support")

    if profile.interdisciplinary_emphasis and "interdisciplinary" in template_strengths:
        score += 1
        reasons.append("Interdisciplinary support")

    if profile.community_connection_desired and "community_connection" in template_strengths:
        score += 1
        reasons.append("Community connection support")
    
    # Subject area alignment
    content_area = str(profile.content_area_focus).lower()
    template_subjects = template_info.get("subject_areas", [])
    
    if content_area in template_subjects or "multiple" in template_subjects:
        score += 2
        reasons.append(f"Subject area alignment ({content_area})")
    
    # Consider constraints
    if profile.resource_limitations_mentioned and template_info.get("complexity") == "high":
        score -= 1
        reasons.append("May be challenging with resource limitations")
    
    if profile.time_constraints_noted and template_info.get("complexity") == "high":
        score -= 1
        reasons.append("May be challenging with time constraints")
    
    return {
        "template_id": template_id,
        "score": score,
        "reasons": reasons,
        "template_name": template_info.get("display_name", template_id)
    }

@design_options_agent.tool
async def create_dimensional_configuration(ctx: RunContext[ProjectDesignContext]) -> Dict[str, Any]:
    """Create dimensional configuration based on project context"""
    
    profile = ctx.deps.project_profile
    
    # Map duration preference to enum
    duration_map = {
        "1-2 days": Duration.SPRINT,
        "1 week": Duration.UNIT, 
        "2-3 weeks": Duration.UNIT,
        "1 month": Duration.JOURNEY,
        "semester": Duration.CAMPAIGN
    }
    
    duration = Duration.UNIT  # default
    for key, value in duration_map.items():
        if key in profile.duration_preference.lower():
            duration = value
            break
    
    # Determine other dimensions based on profile
    social_structure = SocialStructure.COLLABORATIVE if profile.collaborative_emphasis else SocialStructure.INDIVIDUAL
    
    cognitive_complexity = CognitiveComplexity.ANALYSIS  # default
    if profile.includes_design_challenge or profile.requires_experimentation:
        cognitive_complexity = CognitiveComplexity.SYNTHESIS
    
    authenticity_level = AuthenticityLevel.APPLIED if profile.community_connection_desired else AuthenticityLevel.ANCHORED
    
    scaffolding_intensity = ScaffoldingIntensity.FACILITATED  # safe default
    
    product_complexity = ProductComplexity.PORTFOLIO  # default
    if profile.includes_design_challenge:
        product_complexity = ProductComplexity.SYSTEM
    
    delivery_mode = DeliveryMode.FACE_TO_FACE  # default assumption
    
    return {
        "duration": duration,
        "social_structure": social_structure,
        "cognitive_complexity": cognitive_complexity,
        "authenticity_level": authenticity_level,
        "scaffolding_intensity": scaffolding_intensity,
        "product_complexity": product_complexity,
        "delivery_mode": delivery_mode,
        "rationale": f"Configuration optimized for {profile.topic} with {profile.duration_preference} duration"
    }

# Main function -> maybe this is the only one we need? here do injection and search for templates
async def create_project_options(context: ProjectDesignContext) -> Dict[str, Any]:
    """Generate project design options based on consolidated context"""
    try:
        logger.info(f"Starting design options for project: {context.project_profile.topic}")
        
        # Run the agent
        result = await design_options_agent.run(
            "For each of 3 options, pick a different template, name it & give rationale, then describe that option’s driving question, end product, skills, objectives, and assessment.",
            deps=context
        )
        
        if not result or not result.output:
            return {"success": False, "error": "Failed to generate design options", "options": None}
        
        return {
            "success": True,
            "options": result.output.model_dump(),
            "project_topic": context.project_profile.topic,
            "template_selected": result.output.selected_template
        }
        
    except Exception as e:
        logger.error(f"Design options generation failed: {str(e)}", exc_info=True)
        return {"success": False, "error": f"Design options failed: {str(e)}", "options": None}