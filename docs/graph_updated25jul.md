graph TD
    START([START]) --> create_project_profile[Create Project Profile]
    
    %% Profile Phase
    create_project_profile --> |route_after_profile| profile_decision{{Profile Complete?}}
    profile_decision -->|No| get_user_input_for_profile
    profile_decision -->|Yes| start_design_phase
    get_user_input_for_profile --> create_project_profile
    
    %% Design Phase - Sequential Processing
    start_design_phase --> get_standards
    get_standards --> get_knowledge_graph
    
    %% Design Validation
    get_knowledge_graph --> validate_design
    
    validate_design --> |route_after_validation| validation_decision{{Design Valid?}}
    validation_decision -->|No| get_user_input_for_design
    validation_decision -->|Yes| create_project_options
    get_user_input_for_design --> start_design_phase
    
    %% Project Selection
    create_project_options --> get_teacher_selection
    get_teacher_selection --> |route_after_selection| selection_decision{{Selection Approved?}}
    selection_decision -->|No| create_project_options
    selection_decision -->|Yes - Curriculum| get_curriculum_plan
    selection_decision -->|Yes - Assessment| get_assessment_plan
    selection_decision -->|Yes - Resources| get_resource_list
    
    %% Development Phase - Component Reviews
    get_curriculum_plan --> curriculum_review
    get_assessment_plan --> assessment_review
    get_resource_list --> resource_review
    
    %% Component Approval Routing
    curriculum_review --> |route_curriculum_approval| curr_decision{{Curriculum Approved?}}
    curr_decision -->|No| curriculum_refinement
    curr_decision -->|Yes| check_components_completion
    curriculum_refinement --> curriculum_review
    
    assessment_review --> |route_assessment_approval| assess_decision{{Assessment Approved?}}
    assess_decision -->|No| assessment_refinement
    assess_decision -->|Yes| check_components_completion
    assessment_refinement --> assessment_review
    
    resource_review --> |route_resource_approval| resource_decision{{Resources Approved?}}
    resource_decision -->|No| resource_refinement
    resource_decision -->|Yes| check_components_completion
    resource_refinement --> resource_review
    
    %% Final Assembly
    check_components_completion --> |check_components_completion| completion_decision{{All Components Complete?}}
    completion_decision -->|No| create_final_unit
    completion_decision -->|Yes| END([END])
    
    create_final_unit --> final_review
    
    %% Final Decision Routing
    final_review --> |route_final_decision| final_decision{{Final Approved?}}
    final_decision -->|Complete| END
    final_decision -->|Global Changes| global_refinement
    final_decision -->|New Selection| get_teacher_selection
    final_decision -->|Clarification| get_user_input_for_final
    
    global_refinement --> final_review
    get_user_input_for_final --> final_review
    
    %% Styling
    classDef userInput fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef startEnd fill:#e8f5e8,stroke:#2e7d32,stroke-width:3px
    
    class get_user_input_for_profile,get_user_input_for_design,get_user_input_for_final userInput
    class profile_decision,validation_decision,selection_decision,curr_decision,assess_decision,resource_decision,completion_decision,final_decision decision
    class START,END startEnd