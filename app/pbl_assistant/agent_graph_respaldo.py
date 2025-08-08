import logging
import sys
from typing import TypedDict, Dict, Any, List, Optional
from typing_extensions import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from langgraph.config import get_stream_writer

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
from app.pbl_assistant.agents.profiling_agent import create_project_profile
from app.pbl_assistant.agents.standards_agent import get_standards
from app.pbl_assistant.agents.knowledge_graph_agent import get_knowledge_graph
from app.pbl_assistant.agents.design_options_agent import create_project_options, ProjectDesignContext

# Import your models
from app.pbl_assistant.models.profiling import (
    TeacherRequest, 
    ProjectDetails, 
    StandardsAlignment, 
    KnowledgeGraphResult
)

# =============================================================================
# STATE DEFINITION
# =============================================================================

class PBLState(TypedDict):
    # User input
    user_input: str
    messages: Annotated[List[bytes], lambda x, y: x + y]
    
    # Progress tracking
    current_phase: str
    
    # Agent results
    profile_data: Optional[Dict[str, Any]]
    profile_complete: bool
    
    standards_data: Optional[Dict[str, Any]]
    standards_complete: bool
    
    kg_data: Optional[Dict[str, Any]]
    kg_complete: bool
    
    design_options: Optional[Dict[str, Any]]
    
    # Error handling
    error_message: Optional[str]

# =============================================================================
# NODE FUNCTIONS
# =============================================================================

async def create_project_profile_node(state: PBLState) -> Dict[str, Any]:
    """Create project profile using the profiling agent."""
    writer = get_stream_writer()
    writer("🔍 Creating project profile...")
    logger.info("--- Entering Profile Creation Node ---")
    
    try:
        user_input = state.get("user_input", "")
        logger.info(f"Input to profiling agent: {user_input}")
        if not user_input:
            return {
                "error_message": "No user input provided",
                "profile_complete": False
            }
        
        # Create TeacherRequest from user input
        teacher_request = TeacherRequest(raw_message=user_input)
        
        # Call your existing profiling agent
        result = await create_project_profile(teacher_request)
        logger.info(f"Output from profiling agent: {result}")
        
        if result.get("success"):
            profile_data = result.get("profile", {})
            
            # Check if profile is complete enough to proceed
            is_complete = bool(
                profile_data.get("topic") and 
                profile_data.get("grade_level") and 
                profile_data.get("content_area_focus")
            )
            
            writer(f"✅ Profile created for: {profile_data.get('topic', 'Unknown topic')}")
            
            return {
                "profile_data": profile_data,
                "profile_complete": is_complete,
                "current_phase": "profile_complete" if is_complete else "profile_incomplete",
                "error_message": None
            }
        else:
            error_msg = result.get("error", "Unknown error in profile creation")
            writer(f"❌ Profile creation failed: {error_msg}")
            return {
                "error_message": error_msg,
                "profile_complete": False
            }
            
    except Exception as e:
        logger.error(f"Error in create_project_profile_node: {str(e)}")
        writer(f"❌ Profile creation error: {str(e)}")
        return {
            "error_message": str(e),
            "profile_complete": False
        }

async def get_user_input_for_profile_node(state: PBLState) -> Dict[str, Any]:
    """Get additional user input for profile completion."""
    logger.info("--- Entering Get User Input for Profile Node ---")
    writer = get_stream_writer()
    
    # Determine what information is missing
    profile_data = state.get("profile_data", {})
    missing_items = []
    
    if not profile_data.get("topic"):
        missing_items.append("project topic")
    if not profile_data.get("grade_level"):
        missing_items.append("grade level")
    if not profile_data.get("content_area_focus"):
        missing_items.append("content area focus")
    if not profile_data.get("duration_preference"):
        missing_items.append("project duration")
    
    missing_text = ", ".join(missing_items) if missing_items else "additional details"
    
    writer(f"📝 I need more information about: {missing_text}")
    
    # Use interrupt to get user input
    value = interrupt({
        "type": "profile_input",
        "message": f"Please provide more details about: {missing_text}",
        "missing_items": missing_items
    })
    
    return {
        "user_input": value,
        "messages": state.get("messages", []) + [str(value).encode()]
    }

async def start_design_phase_node(state: PBLState) -> Dict[str, Any]:
    """Start the design phase."""
    logger.info("--- Entering Start Design Phase Node ---")
    writer = get_stream_writer()
    writer("🚀 Starting design phase - analyzing standards...")
    
    return {
        "current_phase": "design",
        "standards_complete": False,
        "kg_complete": False
    }

async def get_standards_node(state: PBLState) -> Dict[str, Any]:
    """Get standards alignment using the standards agent."""
    logger.info("--- Entering Standards Alignment Node ---")
    writer = get_stream_writer()
    writer("📚 Aligning to standards...")
    
    try:
        profile_data = state.get("profile_data")
        if not profile_data:
            return {
                "error_message": "Profile data not available for standards alignment",
                "standards_complete": False
            }
            
        # Create ProjectDetails object from the dictionary
        profile = ProjectDetails(**profile_data)
        logger.info(f"Input to standards agent (profile): {profile.model_dump_json(indent=2)}")
        
        # Call your existing standards agent
        result = await get_standards(profile)
        logger.info(f"Output from standards agent: {result}")
        
        if result.get("success"):
            standards_data = result.get("alignment", {})
            writer(f"✅ Standards aligned: {len(standards_data.get('standards', []))} standards found")
            
            return {
                "standards_data": standards_data,
                "standards_complete": True,
                "error_message": None
            }
        else:
            error_msg = result.get("error", "Unknown error in standards analysis")
            writer(f"❌ Standards analysis failed: {error_msg}")
            return {
                "error_message": error_msg,
                "standards_complete": False
            }
            
    except Exception as e:
        logger.error(f"Error in get_standards_node: {str(e)}")
        writer(f"❌ Standards analysis error: {str(e)}")
        return {
            "error_message": str(e),
            "standards_complete": False
        }

async def get_knowledge_graph_node(state: PBLState) -> Dict[str, Any]:
    """Get knowledge graph insights using the knowledge graph agent."""
    logger.info("--- Entering Knowledge Graph Node ---")
    writer = get_stream_writer()
    writer("🧠 Building knowledge graph...")
    
    try:
        standards_data = state.get("standards_data")
        if not standards_data:
            return {
                "error_message": "Standards data not available for knowledge graph",
                "kg_complete": False
            }
            
        # Create StandardsAlignment object from the dictionary
        standards = StandardsAlignment(**standards_data)
        logger.info(f"Input to KG agent (standards): {standards.model_dump_json(indent=2)}")
        
        # Call your existing knowledge graph agent
        result = await get_knowledge_graph(standards)
        logger.info(f"Output from KG agent: {result}")
        
        if result.get("success"):
            kg_data = result.get("kg_insights", {})
            writer(f"✅ Knowledge connections found: {len(kg_data.get('topics', []))} topic areas")
            
            return {
                "kg_data": kg_data,
                "kg_complete": True,
                "error_message": None
            }
        else:
            error_msg = result.get("error", "Unknown error in knowledge graph analysis")
            writer(f"❌ Knowledge graph analysis failed: {error_msg}")
            return {
                "error_message": error_msg,
                "kg_complete": False
            }
            
    except Exception as e:
        logger.error(f"Error in get_knowledge_graph_node: {str(e)}")
        writer(f"❌ Knowledge graph analysis error: {str(e)}")
        return {
            "error_message": str(e),
            "kg_complete": False
        }

async def validate_design_node(state: PBLState) -> Dict[str, Any]:
    """Validate that both standards and knowledge graph are complete."""
    logger.info("--- Entering Validate Design Node ---")
    writer = get_stream_writer()
    
    standards_complete = state.get("standards_complete", False)
    kg_complete = state.get("kg_complete", False)
    
    if standards_complete and kg_complete:
        writer("✅ Design validation complete - ready to create project options")
        return {
            "current_phase": "design_complete"
        }
    else:
        missing = []
        if not standards_complete:
            missing.append("standards")
        if not kg_complete:
            missing.append("knowledge graph")
        
        writer(f"⏳ Waiting for: {', '.join(missing)}")
        return {
            "current_phase": "design_pending",
            "error_message": f"Missing required components: {', '.join(missing)}"
        }

async def get_user_input_for_design_node(state: PBLState) -> Dict[str, Any]:
    """Get user input for design clarification."""
    logger.info("--- Entering Get User Input for Design Node ---")
    writer = get_stream_writer()
    
    # Determine what design issues need clarification
    error_message = state.get("error_message", "")
    
    writer(f"🤔 I need clarification about the design: {error_message}")
    
    # Use interrupt to get user input
    value = interrupt({
        "type": "design_input",
        "message": f"Please clarify the design requirements: {error_message}",
        "context": "design_refinement"
    })
    
    return {
        "user_input": value,
        "messages": state.get("messages", []) + [str(value).encode()],
        "error_message": None  # Clear the error after getting input
    }

async def create_project_options_node(state: PBLState) -> Dict[str, Any]:
    """Create project options using the design options agent."""
    logger.info("--- Entering Project Options Node ---")
    writer = get_stream_writer()
    writer("🎨 Designing project options...")
    
    try:
        profile_data = state.get("profile_data")
        standards_data = state.get("standards_data")
        kg_data = state.get("kg_data")
        
        if not all([profile_data, standards_data, kg_data]):
            return {"error_message": "Missing data for creating project options"}
            
        # Create the context object
        context = ProjectDesignContext(
            profile=ProjectDetails(**profile_data),
            standards=StandardsAlignment(**standards_data),
            knowledge_graph=KnowledgeGraphResult(**kg_data)
        )
        logger.info(f"Input to design options agent (context): {context.model_dump_json(indent=2)}")
        
        # Call the design options agent
        result = await create_project_options(context)
        logger.info(f"Output from design options agent: {result}")
        
        if result.get("success"):
            options_data = result.get("options", {})
            writer(f"✅ Created {len(options_data.get('project_options', []))} project options")
            
            return {
                "design_options": options_data,
                "current_phase": "options_complete"
            }
        else:
            error_msg = result.get("error", "Unknown error in project options creation")
            writer(f"❌ Project options creation failed: {error_msg}")
            return {
                "error_message": error_msg,
                "design_options": None
            }
            
    except Exception as e:
        logger.error(f"Error in create_project_options_node: {str(e)}")
        writer(f"❌ Project options creation error: {str(e)}")
        return {
            "error_message": str(e),
            "design_options": None
        }

# =============================================================================
# ROUTING FUNCTIONS
# =============================================================================

def route_after_profile(state: PBLState) -> str:
    """Route after profile creation."""
    logger.info("--- Routing after profile creation ---")
    if state.get("profile_complete"):
        logger.info("Profile complete. Routing to design phase.")
        return "start_design_phase"
    else:
        logger.info("Profile incomplete. Routing to get user input.")
        return "get_user_input_for_profile"

def route_after_validation(state: PBLState) -> str:
    """Route after design validation."""
    logger.info("--- Routing after design validation ---")
    standards_ok = state.get("standards_complete")
    kg_ok = state.get("kg_complete")
    logger.info(f"Standards complete: {standards_ok}, KG complete: {kg_ok}")
    
    if standards_ok and kg_ok:
        logger.info("Design valid. Routing to create project options.")
        return "create_project_options"
    else:
        logger.info("Design invalid/incomplete. Routing to get user input.")
        # If either is incomplete, we need more user input.
        # This could be more granular in a real application.
        return "get_user_input_for_design"
    
    # This shouldn't happen with the sequential flow, but as a safety
    return "get_user_input_for_design"

# =============================================================================
# GRAPH BUILDER
# =============================================================================

def build_pbl_agent_graph():
    """Build and return the PBL agent graph."""
    # Create the graph with our state
    graph = StateGraph(PBLState)
    
    # Add all nodes
    graph.add_node("create_project_profile", create_project_profile_node)
    graph.add_node("get_user_input_for_profile", get_user_input_for_profile_node)
    graph.add_node("start_design_phase", start_design_phase_node)
    graph.add_node("get_standards", get_standards_node)
    graph.add_node("get_knowledge_graph", get_knowledge_graph_node)
    graph.add_node("validate_design", validate_design_node)
    graph.add_node("get_user_input_for_design", get_user_input_for_design_node)
    graph.add_node("create_project_options", create_project_options_node)
    
    # Build the graph structure - SEQUENTIAL FLOW as per your diagram
    graph.add_edge(START, "create_project_profile")
    
    # Profile phase routing
    graph.add_conditional_edges(
        "create_project_profile",
        route_after_profile,
        {
            "get_user_input_for_profile": "get_user_input_for_profile",
            "start_design_phase": "start_design_phase"
        }
    )
    graph.add_edge("get_user_input_for_profile", "create_project_profile")
    
    # Design phase - SEQUENTIAL execution (standards -> knowledge graph)
    graph.add_edge("start_design_phase", "get_standards")
    graph.add_edge("get_standards", "get_knowledge_graph")
    graph.add_edge("get_knowledge_graph", "validate_design")
    
    # Design validation routing
    graph.add_conditional_edges(
        "validate_design",
        route_after_validation,
        {
            "create_project_options": "create_project_options",
            "get_user_input_for_design": "get_user_input_for_design"
        }
    )
    graph.add_edge("get_user_input_for_design", "start_design_phase")
    
    # End at project options
    graph.add_edge("create_project_options", END)
    
    # Compile the graph with memory
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

# =============================================================================
# MAIN EXECUTION FUNCTION
# =============================================================================

async def run_pbl_agent(user_input: str, thread_id: str = "default") -> Dict[str, Any]:
    """
    Run the PBL agent with the given user input.
    
    Args:
        user_input: The teacher's project request
        thread_id: Thread ID for conversation memory
        
    Returns:
        Dict containing the final result
    """
    logger.info(f"--- Running PBL Agent with utterance: {user_input} ---")
    # Build the graph
    graph = build_pbl_agent_graph()
    
    # Initialize the state
    initial_state = {
        "user_input": user_input,
        "messages": [],
        "current_phase": "profile",
        "profile_data": None,
        "profile_complete": False,
        "standards_data": None,
        "standards_complete": False,
        "kg_data": None,
        "kg_complete": False,
        "design_options": None,
        "error_message": None
    }
    
    try:
        # Run the graph
        config = {"configurable": {"thread_id": thread_id}}
        
        # For streaming execution
        result = None
        async for event in graph.astream(initial_state, config):
            if event and isinstance(event, dict):
                for node_name, node_result in event.items():
                    logger.info(f"Node {node_name} completed")
                    if node_name == "create_project_options" and node_result.get("design_options"):
                        result = node_result
        
        return {
            "success": True,
            "result": result,
            "design_options": result.get("design_options") if result else None
        }
        
    except Exception as e:
        logger.error(f"Error running PBL agent: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "design_options": None
        }

# =============================================================================
# EXAMPLE USAGE
# =============================================================================

async def main():
    """Example usage of the PBL agent graph."""
    user_input = """
    I want to create a science project for 5th grade students about renewable energy. 
    The project should last about 3 weeks and involve hands-on activities. 
    Students should create some kind of presentation or model at the end.
    """

    logger.info(f"--- TEEEESSTT: {user_input} ---")

    
    result = await run_pbl_agent(user_input)
    
    if result["success"]:
        design_options = result.get("design_options", {})
        project_options = design_options.get("project_options", [])
        
        print("🎉 PBL Agent completed successfully!")
        print(f"Generated {len(project_options)} project options:")
        
        for i, option in enumerate(project_options, 1):
            print(f"\n{i}. {option.get('title', 'Untitled Project')}")
            print(f"   Focus: {option.get('focus_approach', 'N/A')}")
            print(f"   Question: {option.get('driving_question', 'N/A')}")
    else:
        print(f"❌ PBL Agent failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

