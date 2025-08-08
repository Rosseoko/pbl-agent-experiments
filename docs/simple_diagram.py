graph TD
    %% Entry Point
    Start([__start__]) --> gather_profile_info
    
    %% Sequential Profiling Phase
    gather_profile_info --> get_next_user_message
    get_next_user_message --> gather_profile_info
    gather_profile_info --> get_standards
    gather_profile_info --> get_framework
    
    %% Parallel Design Phase
    get_standards --> get_knowledge_graph
    get_framework --> create_project_options
    get_knowledge_graph --> create_project_options
    
    %% Teacher Selection
    create_project_options --> get_teacher_selection
    get_teacher_selection --> get_curriculum_plan
    get_teacher_selection --> get_assessment_plan
    get_teacher_selection --> get_resource_list
    
    %% Parallel Development Phase
    get_curriculum_plan --> create_final_unit
    get_assessment_plan --> create_final_unit
    get_resource_list --> create_final_unit
    
    %% Refinement Loop
    create_final_unit --> get_teacher_feedback
    get_teacher_feedback --> |"Needs refinement"| refine_unit
    get_teacher_feedback --> |"Approved"| End([__end__])
    refine_unit --> create_final_unit
    
    %% Styling
    classDef parallel fill:#E8F5E8,stroke:#4CAF50,stroke-width:3px
    classDef sequential fill:#E3F2FD,stroke:#2196F3,stroke-width:3px
    classDef human fill:#FFF3E0,stroke:#FF9800,stroke-width:3px
    classDef final fill:#E0F2F1,stroke:#009688,stroke-width:3px
    classDef refinement fill:#FCE4EC,stroke:#E91E63,stroke-width:3px
    
    class get_standards,get_framework,get_curriculum_plan,get_assessment_plan,get_resource_list parallel
    class gather_profile_info,create_project_options,create_final_unit,refine_unit sequential
    class get_next_user_message,get_teacher_selection,get_teacher_feedback human
    class create_final_unit final
    class get_teacher_feedback,refine_unit refinement