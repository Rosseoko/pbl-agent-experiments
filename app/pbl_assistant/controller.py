from fastapi import APIRouter, HTTPException, status
import logging
from typing import Dict, Any, Optional
from app.pbl_assistant.models.profiling import (
    TeacherRequest,
    ProjectDetails,
    StandardsAlignment
)
from app.pbl_assistant.agents.profiling_agent import create_project_profile
from app.pbl_assistant.agents.standards_agent import get_standards
from app.pbl_assistant.agents.knowledge_graph_agent import get_knowledge_graph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

#Profiling
@router.post("/profiling", response_model=Dict[str, Any])
async def create_profiling_endpoint(request: TeacherRequest):
    """
    Endpoint to analyze a teacher's project request and return a project profile.
    
    Args:
        request: TeacherRequest containing the raw message with project details
        
    Returns:
        Dict containing the project profile with analysis results
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    logger.info(f"Received request: {request.dict()}")
    
    try:
        logger.info("Starting project profiling...")
        # Ensure we only pass the raw_message to the service
        if not request.raw_message:
            raise HTTPException(status_code=400, detail="raw_message is required")
            
        result = await create_project_profile(request)
        logger.info("Successfully created project profile")

        if not result.get("success", True):
            error_msg = result.get("error", "Failed to create project profile")
            logger.error(f"Error in project creation: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Extract the profile and convert it to a dictionary
        profile_result = result.get("profile")
        if hasattr(profile_result, "dict"):
            profile_result = profile_result.dict()
            
        logger.debug(f"Returning result: {profile_result}")
        return {
            "success": True,
            "profile": profile_result
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
        
    except Exception as e:
        error_msg = f"Unexpected error processing request: {str(e)}"
        logger.exception(error_msg)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

# Standards Endpoint
@router.post("/standards", response_model=Dict[str, Any])
async def get_standards_endpoint(project_profile: Dict[str, Any]):
    """
    Endpoint to get standards alignment for a project profile.
    
    Args:
        project_profile: Dictionary containing project profile information
        
    Returns:
        Dict containing the standards alignment results
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    logger.info("Received standards alignment request")
    
    try:
        # Validate required fields
        required_fields = ["topic", "grade_level", "content_area_focus"]
        missing_fields = [field for field in required_fields if field not in project_profile]
        
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
            
        logger.info(f"Processing standards alignment for project: {project_profile.get('topic')}")
        
        # Convert the input dictionary to a ProjectDetails model
        try:
            profile = ProjectDetails(**project_profile)
        except Exception as e:
            error_msg = f"Invalid project profile data: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_msg
            )
        
        # Get standards alignment
        result = await get_standards(profile)
        
        if not result.get("success", False):
            error_msg = result.get("error", "Failed to generate standards alignment")
            logger.error(f"Error in standards alignment: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        logger.info("Successfully generated standards alignment")
        return {
            "success": True,
            "alignment": result.get("alignment", {}),
            "project_topic": project_profile.get("topic"),
            "contextualization": result.get("contextualization", ""),
            "teacher_request": result.get("teacher_request", ""),
            "original_utterance": project_profile.get("original_utterance", "")
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error in get_standards_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while processing standards alignment: {str(e)}"
        )

# Knowledge Graph Endpoint
@router.post("/knowledge_graph", response_model=Dict[str, Any])
async def get_knowledge_graph_endpoint(
    standards_alignment: Dict[str, Any],
    standard_code: Optional[str] = None
):
    """
    Endpoint to get knowledge graph relationships for standards alignment.
    
    Args:
        standards_alignment: Dictionary containing standards alignment information
        standard_code: Optional specific standard code to analyze (defaults to first standard)
        
    Returns:
        Dict containing the knowledge graph relationships and insights
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    logger.info("Received knowledge graph relationship request")
    
    try:
        # Validate required fields
        if not standards_alignment.get("standards"):
            error_msg = "No standards found in the alignment data"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
            
        logger.info(f"Processing knowledge graph for standard: {standard_code or 'first standard'}")
        
        # Convert the input dictionary to a StandardsAlignment model
        try:
            alignment = StandardsAlignment(**standards_alignment)
        except Exception as e:
            error_msg = f"Invalid standards alignment data: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_msg
            )
        
        # Get knowledge graph relationships
        result = await get_knowledge_graph(alignment, standard_code)
        
        if not result.get("success", False):
            error_msg = result.get("error", "Failed to generate knowledge graph relationships")
            logger.error(f"Error in knowledge graph generation: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        logger.info("Successfully generated knowledge graph relationships")
        return {
            "success": True,
            "kg_insights": result.get("kg_insights", {}),
            "standard_analyzed": result.get("standard_analyzed"),
            "project_context": standards_alignment.get("project_context", "")
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error in get_knowledge_graph_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while processing knowledge graph relationships: {str(e)}"
        )
        
# Design Options Endpoint
@router.post("/design_options", response_model=Dict[str, Any])
async def get_design_options_endpoint(
    project_context: Dict[str, Any]
):
    """
    Endpoint to generate project design options based on project context.
    
    Args:
        project_context: Dictionary containing project profile, standards alignment, and knowledge graph insights
        
    Returns:
        Dict containing the generated project design options
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    logger.info("Received design options request")
    
    try:
        # Validate required fields
        required_fields = ["project_profile", "standards_alignment", "kg_insights"]
        for field in required_fields:
            if field not in project_context:
                error_msg = f"Missing required field: {field}"
                logger.error(error_msg)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
        
        logger.info(f"Processing design options for project: {project_context.get('project_profile', {}).get('topic', 'Unknown')}")
        
        # Convert the input dictionary to a ProjectDesignContext model
        try:
            # Import directly from the agent module
            from app.pbl_assistant.agents.design_options_agent import ProjectDesignContext, create_project_options
            
            # Create the context with proper models
            from app.pbl_assistant.models.profiling import ProjectDetails, StandardsAlignment, KnowledgeGraphResult
            
            # First convert the dictionaries to the appropriate model objects
            project_profile = ProjectDetails(**project_context["project_profile"])
            standards_alignment = StandardsAlignment(**project_context["standards_alignment"])
            kg_insights = KnowledgeGraphResult(**project_context["kg_insights"])
            
            # Then create the context
            context = ProjectDesignContext(
                project_profile=project_profile,
                standards_alignment=standards_alignment,
                kg_insights=kg_insights
            )
        except Exception as e:
            error_msg = f"Invalid project context data: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_msg
            )
        
        # Generate design options
        result = await create_project_options(context)
        
        if not result.get("success", False):
            error_msg = result.get("error", "Failed to generate design options")
            logger.error(f"Error in design options generation: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        logger.info("Successfully generated design options")
        return {
            "success": True,
            "options": result.get("options", {}),
            "selected_template": result.get("template_selected", ""),
            "project_topic": result.get("project_topic", "")
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error in get_design_options_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while processing design options: {str(e)}"
        )