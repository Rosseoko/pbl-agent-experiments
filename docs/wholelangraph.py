from typing import TypedDict, Dict, Any, List, Optional, Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from langgraph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# =============================================================================
# PYDANTIC MODELS FOR INTERRUPTS
# =============================================================================

class TeacherSelection(BaseModel):
    selected_project: Dict[str, Any]
    confident: bool
    feedback: Optional[str] = None

class ProfileInput(BaseModel):
    user_input: str
    complete: bool = False
    needs_clarification: Optional[str] = None

class ValidationDecision(BaseModel):
    is_valid: bool
    issues: List[str] = []
    needs_revision: bool = False

class FinalReviewDecision(BaseModel):
    approved: bool
    revision_type: Optional[str] = None  # "global", "selection", "clarification"
    feedback: Optional[str] = None

# =============================================================================
# STATE CONTAINERS (PARTITIONED STATE)
# =============================================================================

class ProfileContainer(TypedDict):
    data: Dict[str, Any]
    complete: bool

class DesignContainer(TypedDict):
    standards: Dict[str, Any]
    knowledge_graph: Dict[str, Any]
    framework: Dict[str, Any]
    validation: Dict[str, Any]
    valid: bool

class DevelopmentContainer(TypedDict):
    curriculum_plan: Dict[str, Any]
    curriculum_approved: bool
    assessment_plan: Dict[str, Any]
    assessment_approved: bool
    resource_list: Dict[str, Any]
    resources_approved: bool

class FinalContainer(TypedDict):
    unit: Dict[str, Any]
    approved: bool
    revision_history: List[Dict[str, Any]]

# =============================================================================
# PROGRESS TRACKER
# =============================================================================

class ProgressTracker(BaseModel):
    current_step: int
    total_steps: int = 12  # Total workflow steps
    phase: str
    estimated_remaining_minutes: int
    completed_components: List[str]
    progress_percentage: int = Field(ge=0, le=100)

def calculate_progress(state: PBLState) -> ProgressTracker:
    """Calculate current progress based on state completion."""
    completed = []
    current_step = 0
    
    # Profile phase (step 1)
    if state.get("profile", {}).get("complete", False):
        completed.append("profile")
        current_step = 1
    
    # Design phase (steps 2-4)
    design = state.get("design", {})
    if design.get("standards"):
        completed.append("standards")
        current_step = 2
    if design.get("knowledge_graph"):
        completed.append("knowledge_graph")
        current_step = 3
    if design.get("framework"):
        completed.append("framework")
        current_step = 4
    if design.get("valid"):
        completed.append("design_validation")
        current_step = 5
    
    # Project selection (step 6)
    if state.get("selected_project"):
        completed.append("project_selection")
        current_step = 6
    
    # Development phase (steps 7-9)
    dev = state.get("development", {})
    if dev.get("curriculum_approved"):
        completed.append("curriculum")
        current_step = 7
    if dev.get("assessment_approved"):
        completed.append("assessment")
        current_step = 8
    if dev.get("resources_approved"):
        completed.append("resources")
        current_step = 9
    
    # Final assembly (steps 10-12)
    final = state.get("final", {})
    if final.get("unit"):
        completed.append("final_unit")
        current_step = 10
    if final.get("approved"):
        completed.append("final_approved")
        current_step = 12
    
    # Determine phase
    if current_step <= 1:
        phase = "Profile Gathering"
    elif current_step <= 5:
        phase = "Design Planning"
    elif current_step == 6:
        phase = "Project Selection"
    elif current_step <= 9:
        phase = "Development"
    else:
        phase = "Final Assembly"
    
    # Estimate remaining time (rough estimates)
    time_per_step = {
        "Profile Gathering": 5,
        "Design Planning": 8,
        "Project Selection": 3,
        "Development": 10,
        "Final Assembly": 7
    }
    
    remaining_steps = 12 - current_step
    estimated_minutes = remaining_steps * time_per_step.get(phase, 5)
    
    return ProgressTracker(
        current_step=current_step,
        phase=phase,
        estimated_remaining_minutes=estimated_minutes,
        completed_components=completed,
        progress_percentage=int((current_step / 12) * 100)
    )

# =============================================================================
# MAIN STATE DEFINITION (PARTITIONED)
# =============================================================================

class PBLState(TypedDict):
    # Core workflow
    current_phase: str
    
    # User interaction
    user_input: str
    messages: Annotated[List[bytes], lambda x, y: x + y]
    
    # Partitioned data containers
    profile: ProfileContainer
    design: DesignContainer
    development: DevelopmentContainer
    final: FinalContainer
    
    # Project selection (kept at root as it's referenced by multiple phases)
    project_options: List[Dict[str, Any]]
    selected_project: Dict[str, Any]
    teacher_confident: bool
    
    # Process tracking
    retry_counts: Dict[str, int]
    progress: ProgressTracker

# =============================================================================
# CENTRALIZED VALIDATION
# =============================================================================

class ValidationResult(BaseModel):
    is_valid: bool
    issues: List[str] = []
    recommendations: List[str] = []
    severity: str = Field(default="info")  # "critical", "warning", "info"

async def validate_component(state: PBLState, component: str, writer) -> Dict[str, Any]:
    """Unified validation for all components."""
    validation_agent = get_validation_agent(component)
    
    if component == "design":
        data = state["design"]
    elif component == "curriculum":
        data = state["development"]["curriculum_plan"]
    elif component == "assessment":
        data = state["development"]["assessment_plan"]
    elif component == "resources":
        data = state["development"]["resource_list"]
    else:
        raise ValueError(f"Unknown component: {component}")
    
    result = await validation_agent.run(data)
    
    return {
        f"{component}_validation": result.model_dump(),
        f"{component}_valid": result.is_valid
    }

# =============================================================================
# CONTEXT-AWARE USER INPUT MANAGEMENT
# =============================================================================

class InputContext(BaseModel):
    source_node: str  # Which node requested more input
    context_message: str
    expected_input_type: str

async def get_user_input_for_profile(state: PBLState, writer) -> Dict[str, Any]:
    """Get additional user input specifically for profile completion."""
    progress = calculate_progress(state)
    writer(f"📊 Progress: {progress.progress_percentage}% - {progress.phase}")
    
    # Context-specific prompting for profile
    value = interrupt({
        "type": "profile_input", 
        "message": "I need more information about your project. Please provide details about grade level, subject, duration, or student needs.",
        "context": "profile_completion"
    })
    user_input = ProfileInput.model_validate(value)
    
    return {
        "user_input": user_input.user_input,
        "messages": state.get("messages", []) + [user_input.user_input.encode()]
    }

async def get_user_input_for_design(state: PBLState, writer) -> Dict[str, Any]:
    """Get additional user input specifically for design validation."""
    progress = calculate_progress(state)
    writer(f"📊 Progress: {progress.progress_percentage}% - {progress.phase}")
    
    design_issues = state.get("design", {}).get("validation", {}).get("issues", [])
    context_message = f"The design needs refinement. Issues found: {', '.join(design_issues)}"
    
    value = interrupt({
        "type": "design_input",
        "message": context_message,
        "context": "design_refinement"
    })
    user_input = ProfileInput.model_validate(value)
    
    return {
        "user_input": user_input.user_input,
        "messages": state.get("messages", []) + [user_input.user_input.encode()]
    }

async def get_user_input_for_final(state: PBLState, writer) -> Dict[str, Any]:
    """Get additional user input for final clarifications."""
    progress = calculate_progress(state)
    writer(f"📊 Progress: {progress.progress_percentage}% - {progress.phase}")
    
    value = interrupt({
        "type": "final_input",
        "message": "I need clarification to finalize your project. What specific changes would you like?",
        "context": "final_clarification"
    })
    user_input = ProfileInput.model_validate(value)
    
    return {
        "user_input": user_input.user_input,
        "messages": state.get("messages", []) + [user_input.user_input.encode()]
    }

# =============================================================================
# ROUTING FUNCTIONS WITH TYPE HINTS
# =============================================================================

def route_after_profile(state: PBLState) -> str:
    """Route after profile gathering - continue gathering or proceed to design."""
    if not state.get("profile", {}).get("complete", False):
        return "get_user_input_for_profile"
    # Start both standards and framework in parallel since profile is complete
    return "start_design_phase"

def route_after_validation(state: PBLState) -> str:
    """Route after design validation."""
    if not state.get("design", {}).get("valid", False):
        return "get_user_input_for_design"
    return "create_project_options"

def route_final_decision(state: PBLState) -> str:
    """Route after final review."""
    if state.get("final", {}).get("approved", False):
        return END
    
    # Check what type of revision is needed
    final_data = state.get("final", {}).get("revision_history", [])
    if final_data:
        last_feedback = final_data[-1]
        revision_type = last_feedback.get("revision_type", "global")
        
        if revision_type == "selection":
            return "get_teacher_selection"
        elif revision_type == "clarification":
            return "get_user_input_for_final"
        else:
            return "global_refinement"
    
    return "global_refinement"

def route_after_selection(state: PBLState) -> Union[str, List[str]]:
    """Route after teacher project selection."""
    if not state.get("teacher_confident", False):
        return "create_project_options"
    # Development components can run in parallel
    return ["get_curriculum_plan", "get_assessment_plan", "get_resource_list"]

def route_curriculum_approval(state: PBLState) -> str:
    """Route after curriculum review."""
    if state.get("development", {}).get("curriculum_approved", False):
        return "check_components_completion"
    return "curriculum_refinement"

def route_assessment_approval(state: PBLState) -> str:
    """Route after assessment review."""
    if state.get("development", {}).get("assessment_approved", False):
        return "check_components_completion"
    return "assessment_refinement"

def route_resource_approval(state: PBLState) -> str:
    """Route after resource review."""
    if state.get("development", {}).get("resources_approved", False):
        return "check_components_completion"
    return "resource_refinement"

def check_components_completion(state: PBLState) -> str:
    """Check if all development components are approved - RENAMED to avoid conflict."""
    dev = state.get("development", {})
    all_approved = (
        dev.get("curriculum_approved", False) and
        dev.get("assessment_approved", False) and
        dev.get("resources_approved", False)
    )
    
    if all_approved:
        return "create_final_unit"
    return END  # Wait for other components

def route_final_decision(state: PBLState) -> str:
    """Route after final review."""
    if state.get("final", {}).get("approved", False):
        return END
    
    # Check what type of revision is needed
    final_data = state.get("final", {}).get("revision_history", [])
    if final_data:
        last_feedback = final_data[-1]
        revision_type = last_feedback.get("revision_type", "global")
        
        if revision_type == "selection":
            return "get_teacher_selection"
        elif revision_type == "clarification":
            return "get_next_user_message"
        else:
            return "global_refinement"
    
    return "global_refinement"

# =============================================================================
# UPDATED NODE FUNCTIONS WITH PYDANTIC INTERRUPTS
# =============================================================================

async def create_project_profile(state: PBLState, writer) -> Dict[str, Any]:
    """Create project profile with progress tracking."""
    progress = calculate_progress(state)
    writer(f"📊 Progress: {progress.progress_percentage}% - {progress.phase}")
    
    async with writer.status("👥 Gathering project profile information..."):
        # Your existing profiling agent work
        user_input = state.get("user_input", "")
        # result = await project_profiling_agent.run(user_input)
        
        # Simulated result for example
        profile_data = {"grade_level": "5", "subject": "science"}
        complete = len(user_input) > 10  # Simple completion check
        
        writer.update("✅ Profile information collected")
    
    updated_progress = calculate_progress({
        **state,
        "profile": {"data": profile_data, "complete": complete}
    })
    
    return {
        "profile": {
            "data": profile_data,
            "complete": complete
        },
        "current_phase": "profile" if not complete else "design",
        "progress": updated_progress
    }

async def start_design_phase(state: PBLState, writer) -> Dict[str, Any]:
    """Coordinate the start of design phase - triggers both standards and framework."""
    progress = calculate_progress(state)
    writer(f"📊 Progress: {progress.progress_percentage}% - Starting Design Phase")
    
    # This node will trigger both get_standards and get_framework to run
    # The actual work is done in those nodes, this just coordinates
    return {
        "current_phase": "design",
        "progress": progress
    }

async def get_teacher_selection(state: PBLState, writer) -> Dict[str, Any]:
    """Handle teacher project selection with Pydantic validation."""
    progress = calculate_progress(state)
    writer(f"📊 Progress: {progress.progress_percentage}% - Project Selection Phase")
    
    # Use Pydantic model for interrupt
    value = interrupt({
        "type": "teacher_selection", 
        "projects": state.get("project_options", [])
    })
    selection = TeacherSelection.model_validate(value)
    
    updated_progress = calculate_progress({
        **state,
        "selected_project": selection.selected_project
    })
    
    return {
        "selected_project": selection.selected_project,
        "teacher_confident": selection.confident,
        "progress": updated_progress
    }

async def final_review(state: PBLState, writer) -> Dict[str, Any]:
    """Final review with Pydantic validation."""
    progress = calculate_progress(state)
    writer(f"📊 Progress: {progress.progress_percentage}% - Final Review")
    
    # Use Pydantic model for interrupt
    value = interrupt({
        "type": "final_review",
        "unit": state.get("final", {}).get("unit", {})
    })
    decision = FinalReviewDecision.model_validate(value)
    
    # Update final container
    final_data = state.get("final", {})
    revision_history = final_data.get("revision_history", [])
    
    if not decision.approved and decision.feedback:
        revision_history.append({
            "revision_type": decision.revision_type,
            "feedback": decision.feedback,
            "timestamp": "now"  # You'd use actual timestamp
        })
    
    updated_final = {
        **final_data,
        "approved": decision.approved,
        "revision_history": revision_history
    }
    
    return {
        "final": updated_final,
        "progress": calculate_progress({**state, "final": updated_final})
    }

# =============================================================================
# PLACEHOLDER NODE FUNCTIONS (implement your existing logic)
# =============================================================================

async def get_standards(state: PBLState, writer) -> Dict[str, Any]:
    """Get standards - needs profile data so can't run in parallel."""
    profile_data = state.get("profile", {}).get("data", {})
    if not profile_data:
        raise ValueError("Profile data required for standards")
    
    # Your existing standards logic here
    standards_data = {"common_core": True}  # Placeholder
    
    design_data = state.get("design", {})
    return {
        "design": {
            **design_data,
            "standards": standards_data
        }
    }

# Add other placeholder functions for completeness
async def get_knowledge_graph(state: PBLState, writer) -> Dict[str, Any]:
    design_data = state.get("design", {})
    return {"design": {**design_data, "knowledge_graph": {"nodes": []}}}

async def get_framework(state: PBLState, writer) -> Dict[str, Any]:
    design_data = state.get("design", {})
    return {"design": {**design_data, "framework": {"pbl_type": "inquiry"}}}

async def validate_design(state: PBLState, writer) -> Dict[str, Any]:
    design_data = state.get("design", {})
    is_valid = bool(design_data.get("standards") and design_data.get("framework"))
    return {"design": {**design_data, "valid": is_valid}}

# Add other placeholder node functions...
async def create_project_options(state: PBLState, writer) -> Dict[str, Any]:
    return {"project_options": [{"title": "Water Cycle Investigation"}]}

async def get_curriculum_plan(state: PBLState, writer) -> Dict[str, Any]:
    dev_data = state.get("development", {})
    return {"development": {**dev_data, "curriculum_plan": {"weeks": 3}}}

async def get_assessment_plan(state: PBLState, writer) -> Dict[str, Any]:
    dev_data = state.get("development", {})
    return {"development": {**dev_data, "assessment_plan": {"rubric": True}}}

async def get_resource_list(state: PBLState, writer) -> Dict[str, Any]:
    dev_data = state.get("development", {})
    return {"development": {**dev_data, "resource_list": {"materials": []}}}

async def curriculum_review(state: PBLState, writer) -> Dict[str, Any]:
    dev_data = state.get("development", {})
    return {"development": {**dev_data, "curriculum_approved": True}}

async def assessment_review(state: PBLState, writer) -> Dict[str, Any]:
    dev_data = state.get("development", {})
    return {"development": {**dev_data, "assessment_approved": True}}

async def resource_review(state: PBLState, writer) -> Dict[str, Any]:
    dev_data = state.get("development", {})
    return {"development": {**dev_data, "resources_approved": True}}

async def curriculum_refinement(state: PBLState, writer) -> Dict[str, Any]:
    return {}  # Refinement logic

async def assessment_refinement(state: PBLState, writer) -> Dict[str, Any]:
    return {}  # Refinement logic

async def resource_refinement(state: PBLState, writer) -> Dict[str, Any]:
    return {}  # Refinement logic

async def create_final_unit(state: PBLState, writer) -> Dict[str, Any]:
    final_data = state.get("final", {})
    return {"final": {**final_data, "unit": {"complete": True}}}

async def global_refinement(state: PBLState, writer) -> Dict[str, Any]:
    return {}  # Global refinement logic

# =============================================================================
# UPDATED GRAPH BUILDER
# =============================================================================

def build_pbl_agent_graph():
    """Build and return the PBL agent graph with improvements."""
    # Create the graph with our partitioned state
    graph = StateGraph(PBLState)
    
    # Add all nodes
    graph.add_node("create_project_profile", create_project_profile)
    
    # Context-specific user input nodes
    graph.add_node("get_user_input_for_profile", get_user_input_for_profile)
    graph.add_node("get_user_input_for_design", get_user_input_for_design)
    graph.add_node("get_user_input_for_final", get_user_input_for_final)
    
    # Design coordination
    graph.add_node("start_design_phase", start_design_phase)
    
    # Design phase nodes
    graph.add_node("get_standards", get_standards)
    graph.add_node("get_knowledge_graph", get_knowledge_graph)
    graph.add_node("get_framework", get_framework)
    graph.add_node("validate_design", validate_design)
    
    # Project selection nodes
    graph.add_node("create_project_options", create_project_options)
    graph.add_node("get_teacher_selection", get_teacher_selection)
    
    # Development phase nodes
    graph.add_node("get_curriculum_plan", get_curriculum_plan)
    graph.add_node("get_assessment_plan", get_assessment_plan)
    graph.add_node("get_resource_list", get_resource_list)
    
    # Review nodes
    graph.add_node("curriculum_review", curriculum_review)
    graph.add_node("assessment_review", assessment_review)
    graph.add_node("resource_review", resource_review)
    
    # Refinement nodes
    graph.add_node("curriculum_refinement", curriculum_refinement)
    graph.add_node("assessment_refinement", assessment_refinement)
    graph.add_node("resource_refinement", resource_refinement)
    
    # Final assembly nodes
    graph.add_node("create_final_unit", create_final_unit)
    graph.add_node("final_review", final_review)
    graph.add_node("global_refinement", global_refinement)
    graph.add_node("check_components_completion", check_components_completion)  # RENAMED
    
    # Build the graph structure
    # Entry point
    graph.add_edge(START, "create_project_profile")
    
    # Profile phase routing - specific input handler for profile issues
    graph.add_conditional_edges(
        "create_project_profile",
        route_after_profile,
        ["get_user_input_for_profile", "start_design_phase"]
    )
    graph.add_edge("get_user_input_for_profile", "create_project_profile")
    
    # Design phase coordination - start both standards and framework in parallel
    graph.add_edge("start_design_phase", "get_standards")
    graph.add_edge("start_design_phase", "get_framework")
    
    # Design phase flow - standards leads to knowledge_graph, framework runs independently
    graph.add_edge("get_standards", "get_knowledge_graph")
    
    # Framework needs to start after profile is complete - add this to profile routing
    # (This will be handled in the profile routing section)
    
    # Both knowledge_graph and framework feed into validation
    graph.add_edge("get_knowledge_graph", "validate_design")
    graph.add_edge("get_framework", "validate_design")
    
    # Validation routing - specific input handler for design issues
    graph.add_conditional_edges(
        "validate_design",
        route_after_validation,
        ["get_user_input_for_design", "create_project_options"]
    )
    graph.add_edge("get_user_input_for_design", "start_design_phase")  # Restart design with new input
    
    # Project selection
    graph.add_edge("create_project_options", "get_teacher_selection")
    graph.add_conditional_edges(
        "get_teacher_selection",
        route_after_selection,
        ["create_project_options", "get_curriculum_plan", "get_assessment_plan", "get_resource_list"]
    )
    
    # Development phase - each component goes to its review
    graph.add_edge("get_curriculum_plan", "curriculum_review")
    graph.add_edge("get_assessment_plan", "assessment_review")
    graph.add_edge("get_resource_list", "resource_review")
    
    # Component approval routing - all point to the RENAMED function
    graph.add_conditional_edges(
        "curriculum_review",
        route_curriculum_approval,
        ["curriculum_refinement", "check_components_completion"]
    )
    graph.add_conditional_edges(
        "assessment_review",
        route_assessment_approval,
        ["assessment_refinement", "check_components_completion"]
    )
    graph.add_conditional_edges(
        "resource_review",
        route_resource_approval,
        ["resource_refinement", "check_components_completion"]
    )
    
    # Refinement loops
    graph.add_edge("curriculum_refinement", "curriculum_review")
    graph.add_edge("assessment_refinement", "assessment_review")
    graph.add_edge("resource_refinement", "resource_review")
    
    # Final assembly and review
    graph.add_conditional_edges(
        "check_components_completion",  # RENAMED function
        check_components_completion,    # Same function, just renamed
        ["create_final_unit", END]
    )
    graph.add_edge("create_final_unit", "final_review")
    
    # Final decision routing - specific input handler for final clarifications
    graph.add_conditional_edges(
        "final_review",
        route_final_decision,
        [END, "global_refinement", "get_teacher_selection", "get_user_input_for_final"]
    )
    graph.add_edge("get_user_input_for_final", "final_review")  # Re-review with clarifications
    graph.add_edge("global_refinement", "final_review")
    
    # Compile the graph with memory
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

# Create the PBL agent graph
pbl_agent_graph = build_pbl_agent_graph()