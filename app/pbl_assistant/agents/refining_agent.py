# app/pbl_assistant/agents/refining_agent.py

from __future__ import annotations

from typing import List, Optional
import os

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from app.pbl_assistant.aws_config import get_bedrock_client

from app.pbl_assistant.models.profiling import (
    ProjectOption,
    StandardsAlignment,
    KnowledgeGraphResult,
)


# ──────────────────────────────────────────────────────────────────────────────
# Result & Deps Models
# ──────────────────────────────────────────────────────────────────────────────

class RefinementResult(BaseModel):
    """
    Structured result returned by the refining agent.
    - updated_project: the full, coherent ProjectOption after applying the change
    - change_summary: brief human-readable summary of what changed and why
    - affected_fields: list of field names that were changed (e.g., ["driving_question", "key_activities"])
    - warnings: optional non-fatal notes (e.g., "no_change_detected", truncations, or assumptions)
    """
    updated_project: ProjectOption = Field(..., description="The fully updated project option.")
    change_summary: str = Field(..., min_length=1, description="1–3 sentences summarizing what changed.")
    affected_fields: List[str] = Field(default_factory=list, description="Canonical field names that were updated.")
    warnings: List[str] = Field(default_factory=list, description="Any non-fatal issues or assumptions.")


class RefinementContext(BaseModel):
    """
    Context passed as `deps` to the refining agent.
    - current_project: the project being edited (required)
    - language: preferred output language (match existing project language; do not translate unless asked)
    - class_profile: optional notes about the classroom; use to keep age/ability fit
    - standards_alignment / knowledge_graph_result: optional to preserve/maintain alignment
    - strict: if True, update ONLY explicitly requested fields (no cascade); if False, allow coherence cascades
    """
    current_project: ProjectOption
    language: Optional[str] = "English"
    class_profile: Optional[str] = None
    standards_alignment: Optional[StandardsAlignment] = None
    knowledge_graph_result: Optional[KnowledgeGraphResult] = None
    strict: bool = False


# ──────────────────────────────────────────────────────────────────────────────
# System Prompt (Full Rewrite + Dependency-Aware)
# ──────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are *Erandi*, an expert curriculum editor that refines structured Project-Based Learning (PBL) plans.

You receive:
  • The teacher's change request (natural language).
  • The CURRENT project (a JSON object with fields like title, driving_question, end_product, key_activities, etc.).
  • Optional context: class_profile, standards_alignment, knowledge_graph_result, language, and a 'strict' flag.

Your job:
  1) IMPLEMENT the teacher’s requested change(s) **exactly**.
  2) Then perform an **impact analysis** and update any **dependent fields** needed to keep the plan coherent.
     Examples of dependencies:
       - driving_question ↔ end_product ↔ key_activities ↔ learning_objectives ↔ assessment_summary/assessment_highlights
       - focus_approach should reflect the new emphasis
       - key_skills should match the changed activities and learning objectives
  3) Return the **ENTIRE** updated project object (full rewrite), **preserving all unrelated fields** unchanged.

CRITICAL RULES:
- Always keep the **language** of the existing content (from 'language' or inferred from the current project).
  DO NOT translate the whole project unless the teacher explicitly asks for it.
- Respect grade level and age appropriateness implied by the existing project and class_profile.
- When the teacher says **add**, append to the corresponding list (do not replace).
- When the teacher says **replace** or **change**, update the targeted field(s).
- When the teacher says **remove**, delete only the specified items.
- Keep the output concise and consistent. Prefer parallel structure and similar tone across fields.

STRICT MODE:
- If `strict=true`, update ONLY the explicitly requested fields. Perform no cascaded changes, unless a field now becomes self-contradictory or nonsensical (in that case, minimally fix and include a warning).

OUTPUT SHAPE (MANDATORY):
Return a JSON object matching the `RefinementResult` schema with:
  - updated_project: the full ProjectOption after changes
  - change_summary: 1–3 sentences describing what changed and why
  - affected_fields: array of field names you updated (e.g., ["driving_question","end_product"])
  - warnings: array of strings, empty if none

QUALITY & CONSISTENCY CHECKS BEFORE RETURNING:
- Ensure the driving_question, end_product, activities, objectives, and assessments are aligned.
- Ensure lists (key_activities, learning_objectives, key_skills, assessment_highlights) do not contain duplicates or empty items.
- Keep titles short and meaningful; keep the driving question under ~180 characters if possible.
- Do NOT invent URLs or external resources; only update what the teacher asked and what coherence demands.

If the teacher’s request implies no meaningful change, return the same project and set warnings=["no_change_detected"].
"""


# ──────────────────────────────────────────────────────────────────────────────
# Agent Definition
# ──────────────────────────────────────────────────────────────────────────────

# Allow model override via env var if desired; default to Haiku for speed/cost parity with your other agents.

refining_agent = Agent[RefinementResult, RefinementContext](
    model=BedrockConverseModel(
        "anthropic.claude-3-sonnet-20240229-v1:0",
        client=get_bedrock_client(),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    ),
    result_type=RefinementResult,
    system_prompt=SYSTEM_PROMPT,
    retries=3,  # be a little forgiving on schema conformance
)