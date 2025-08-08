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