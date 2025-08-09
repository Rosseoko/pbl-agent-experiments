import logging
import os
from typing import List, Dict, Any, Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.bedrock import BedrockConverseModel
from app.pbl_assistant.aws_config import get_bedrock_client

from app.pbl_assistant.models.profiling import (
    ProjectDetails, 
    StandardsAlignment, 
)

# Simple, focused standards agent
standards_agent = Agent(
    model=BedrockConverseModel(
        "anthropic.claude-3-haiku-20240307-v1:0",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    ),
    deps_type=ProjectDetails,
    result_type=StandardsAlignment,
    result_retries=3,
    system_prompt="""Your name is Erandi, you are an energetic and friendly standards alignment expert for Project-Based Learning.

Your task: Create a comprehensive standards alignment for the given project.

KEY RULES:
1. If standard codes are provided - validate them using validate_standards tool and suggest corrections if needed
2. If no standard codes - recommend appropriate standards based on topic/grade using recommend_standards tool
3. All standards MUST match the project's grade level
4. Focus on NGSS and Common Core standards
5. Make learning objectives specific to the project topic and end product

OUTPUT: Valid StandardsAlignment JSON with contextualized standards, objectives, and assessments."""
)

@standards_agent.tool
async def validate_standards(ctx: RunContext[ProjectDetails], codes: List[str]) -> Dict[str, Any]:
    """Validate provided standard codes and check grade level alignment."""
    project = ctx.deps
    results = {}
    
    for code in codes:
        result = {
            "is_valid": True,
            "grade_match": True,
            "issues": [],
            "suggested_correction": None
        }
        
        # Basic validation - let LLM handle the complex logic
        # Just flag obvious grade mismatches
        project_grades = str(project.grade_level).split(',') if project.grade_level else []
        
        # Simple grade checking for common patterns
        if code.startswith('K-') and '0' not in str(project.grade_level):
            result["grade_match"] = False
            result["issues"].append(f"Kindergarten standard for grade {project.grade_level}")
        elif '-' in code and code[0].isdigit():
            standard_grade = code.split('-')[0]
            if standard_grade not in str(project.grade_level):
                result["grade_match"] = False
                result["issues"].append(f"Grade {standard_grade} standard for grade {project.grade_level}")
        
        results[code] = result
    
    return results

@standards_agent.tool
async def find_standards_by_content(ctx: RunContext[ProjectDetails]) -> Dict[str, Any]:
    """Find appropriate standards based on project content and grade level."""
    project = ctx.deps
    
    return {
        "topic": project.topic,
        "grade_level": project.grade_level,
        "content_area": project.content_area_focus,
        "end_product": project.end_product,
        "includes_design": project.includes_design_challenge,
        "requires_experimentation": project.requires_experimentation,
        "involves_data": project.involves_data_collection,
        "needs_math": project.needs_mathematical_analysis,
        "message": f"Find grade-appropriate standards for {project.topic} project at grade {project.grade_level}"
    }

async def get_standards(project: ProjectDetails) -> Dict[str, Any]:
    """Get standards alignment for a project."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Getting standards for project: {project.topic}")
        
        # Simple message - let the agent decide what to do based on project details
        message = "Create standards alignment for this project."
        if project.standard_codes:
            message += f" Validate these provided standards: {', '.join(project.standard_codes)}"
        else:
            message += " Find appropriate standards based on the project content."
        
        result = await standards_agent.run(message, deps=project)
        
        if not result or not result.data:
            return {
                "success": False, 
                "error": "Failed to create standards alignment", 
                "alignment": None
            }
        
        return {
            "success": True,
            "alignment": result.data.model_dump() if hasattr(result.data, 'model_dump') else result.data,
            "project_topic": project.topic,
            "grade_level": project.grade_level
        }
        
    except Exception as e:
        logger.error(f"Standards alignment error: {str(e)}", exc_info=True)
        return {
            "success": False, 
            "error": f"Standards alignment failed: {str(e)}", 
            "alignment": None
        }