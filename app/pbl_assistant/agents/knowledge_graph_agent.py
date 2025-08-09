import logging
import os
from typing import Dict, Any, Optional, List
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic import ValidationError
import asyncio
from app.pbl_assistant.aws_config import get_bedrock_client

from app.pbl_assistant.models.profiling import StandardsAlignment, KnowledgeGraphResult

logger = logging.getLogger(__name__)

# Fixed KG agent with explicit instructions
kg_agent = Agent(
    model=BedrockConverseModel(
        "anthropic.claude-3-sonnet-20240229-v1:0",
        client=get_bedrock_client(),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    ),
    deps_type=StandardsAlignment,
    result_type=KnowledgeGraphResult,
    result_retries=3,
    system_prompt="""
Your name is Erandi, you are an energetic and friendly expert in PBL design and knowledge graphs.  
Only analyze the single standard I provide; do not introduce or fetch any other standard codes.
You receive a StandardsAlignment JSON containing one or more standards with:
  • code
  • description
  • grade_level

Your job is to produce a **KnowledgeGraphResult** with *non-empty* fields nd relate all insights to the project topic and the standard:

1. **standard_code** and **standard_description**: exactly copy from the primary standard.  
2. **project_topics** (3 entries): each a dict with  
   – name: a key concept or theme directly tied to the standard  
   – description: 1–2 sentence elaboration of that concept  
3. **cross_subject_connections** (2 entries): each a dict with  
   – subject: another discipline  
   – connection: how that discipline naturally integrates with this standard  
4. **real_world_applications** (2 entries): each a dict with  
   – application: a real-world use or context  
   – details: why it matters to this standard  
   - related UN SDGs: 2 entries, each a dict. Important!
5. **curriculum_resources** (2 entries): each a dict with  
   – title: name of a high-quality resource (e.g. NASA website, interactive sim)  
   – url: its link  
6. **pbl_integration_ideas** (3 entries): short bullet ideas for project-based activities.  
7. **relevance_confidence**: a number between 0.0 and 1.0 indicating your confidence.

Return strictly valid JSON matching the KnowledgeGraphResult model. Do **not** leave any of the above lists empty.
"""
)