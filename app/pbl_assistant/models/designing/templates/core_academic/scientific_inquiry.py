# templates/core_academic/scientific_inquiry.py

from pydantic import Field
from typing import List, Dict
from app.pbl_assistant.models.designing.core.base_template import (
    BaseTemplate, EntryEventFramework, AssessmentFramework,
    InquiryFramework, LearningEnvironmentFramework, StudentAgencyFramework,
    DocumentationFramework, ExpressionPathways, EmergentLearningSupport,
    EntryEventOption, MilestoneTemplate, FormativeAssessmentTool,
    SummativeAssessmentMoment, ReflectionProtocol, AuthenticAudienceFramework,
    HQPBLAlignment, CompatibilityMatrix
)
from app.pbl_assistant.models.designing.core.enums import (
    TemplateIntent, Duration, SocialStructure, CognitiveComplexity,
    AuthenticityLevel, ScaffoldingIntensity, ProductComplexity, DeliveryMode, SubjectArea
)

TEMPLATE = create_scientific_inquiry_template = BaseTemplate(
    template_id="scientific_inquiry",
    intent=TemplateIntent.SCIENTIFIC_INQUIRY,
    display_name="Scientific Inquiry Project",
    description="Students ask questions, run experiments, and learn to think like scientists.",
    pedagogical_approach="Inquiry-based learning through hands-on experiments",
    comprehensive_overview=(
        "In this project, students become young scientists. They start with a curious question, "
        "plan a simple experiment, gather materials, collect and record data, analyze what happens, "
        "and then share their discoveries. Along the way they learn to observe carefully, make fair tests, "
        "and explain their results."
    ),
    driving_question_template="How can we use an experiment to answer [our science question]?",
    
    core_learning_cycle=[
        "Ask & Wonder",
        "Plan Experiment",
        "Do & Observe",
        "Collect & Analyze Data",
        "Share & Reflect"
    ],
    
    essential_skills=[
        "question_formulation",
        "hypothesis_development",
        "experiment_planning",
        "data_collection",
        "data_analysis",
        "conclusion_drawing",
        "presentation",
        "reflection"
    ],
    
    required_components=[
        "driving_question",
        "hypothesis",
        "materials_list",
        "procedure_steps",
        "data_records",
        "conclusion",
        "reflection_notes"
    ],
    
    natural_subject_areas=[
        SubjectArea.SCIENCE,
        SubjectArea.MATHEMATICS
    ],
    
    cross_curricular_connections=[
        "Reading and following instructions",
        "Writing clear experiment steps",
        "Measuring and recording data",
        "Drawing diagrams",
        "Working in teams"
    ],
    
    entry_event_framework=EntryEventFramework(
        purpose="Spark curiosity with a fun, safe science demo",
        design_principles=[
            "Use a simple, hands-on demonstration",
            "Choose bright, visible effects",
            "Encourage ‘I wonder…’ questions",
            "Connect to things students see every day"
        ],
        template_options=[
            EntryEventOption(
                type="magic_milk_demo",
                example="Drop food coloring into milk and add dish soap to see colors swirl",
                student_response_pattern="Watch → ask questions → talk with partner",
                question_generation_method="What do you notice? What might happen if we change X?",
                estimated_time="20 minutes",
                materials_needed=["Milk", "Food coloring", "Dish soap", "Cotton swabs"]
            ),
            EntryEventOption(
                type="mystery_mixture",
                example="Mix baking soda and vinegar in a small container and watch it fizz",
                student_response_pattern="Observe → record what happens → discuss",
                question_generation_method="Why does it bubble? What if we used more vinegar?",
                estimated_time="15 minutes",
                materials_needed=["Baking soda", "Vinegar", "Plastic cups", "Spoons"]
            )
        ],
        customization_guidance="Pick a demo that fits your classroom space and safety guidelines"
    ),
    
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Ask & Wonder",
            learning_purpose="Students choose a question and make a guess (hypothesis)",
            core_activities=[
                "Brainstorm science questions",
                "Use question starters (What happens if…? How does…? Why does…?)",
                "Pick one question and write it down",
                "Make a hypothesis (a guess)"
            ],
            essential_deliverables=[
                "Written driving question",
                "Hypothesis statement"
            ],
            reflection_checkpoints=[
                "Is our question testable?",
                "What do we expect will happen?"
            ],
            duration_scaling_notes="Sprint: Question only; Unit: Add hypothesis"
        ),
        MilestoneTemplate(
            milestone_name="Plan Experiment",
            learning_purpose="Decide what to test and how",
            core_activities=[
                "List materials needed",
                "Write step-by-step procedure",
                "Identify what to change (variable) and what to keep the same",
                "Plan how to record results"
            ],
            essential_deliverables=[
                "Materials list",
                "Procedure steps"
            ],
            reflection_checkpoints=[
                "Do we have everything we need?",
                "Is our procedure clear?"
            ],
            duration_scaling_notes="Sprint: Draft list; Unit: Complete procedure"
        ),
        MilestoneTemplate(
            milestone_name="Do & Observe",
            learning_purpose="Carry out the experiment safely and watch closely",
            core_activities=[
                "Follow procedure steps",
                "Observe and talk about what you see",
                "Take photos or draw pictures",
                "Record initial observations"
            ],
            essential_deliverables=[
                "Photos or drawings of experiment",
                "Observation notes"
            ],
            reflection_checkpoints=[
                "What do you notice first?",
                "Any surprises?"
            ],
            duration_scaling_notes="Same activities; vary number of trials"
        ),
        MilestoneTemplate(
            milestone_name="Collect & Analyze Data",
            learning_purpose="Write down measurements and look for patterns",
            core_activities=[
                "Use tables or charts to record data",
                "Count or measure results",
                "Make simple graphs or diagrams",
                "Discuss patterns in small groups"
            ],
            essential_deliverables=[
                "Completed data table",
                "Simple graph or chart"
            ],
            reflection_checkpoints=[
                "What does our data show?",
                "Does it match our hypothesis?"
            ],
            duration_scaling_notes="Sprint: One trial; Unit: Two trials; Journey: Multiple trials"
        ),
        MilestoneTemplate(
            milestone_name="Share & Reflect",
            learning_purpose="Tell others what you learned and think about why it matters",
            core_activities=[
                "Prepare a short talk or poster",
                "Explain your experiment, data, and conclusion",
                "Write a reflection on what you would try next"
            ],
            essential_deliverables=[
                "Poster or slides",
                "Oral presentation notes",
                "Reflection journal entry"
            ],
            reflection_checkpoints=[
                "How well did our experiment work?",
                "What would we change next time?"
            ],
            duration_scaling_notes="Same steps; depth varies by duration"
        )
    ],
    
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Hypothesis Check",
                purpose="Ensure hypothesis is clear and testable",
                implementation_guidance="Teacher reviews and gives feedback",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After planning",
                    Duration.JOURNEY: "Weekly",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Simple thumbs up/down",
                    Duration.UNIT: "Written feedback",
                    Duration.JOURNEY: "Peer and teacher feedback",
                    Duration.CAMPAIGN: "Rubric and peer review"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Procedure Check",
                purpose="Check that steps are clear and safe",
                implementation_guidance="Safety and clarity review before starting",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "After each trial",
                    Duration.CAMPAIGN: "Weekly check"
                },
                scaling_guidance={
                    Duration.SPRINT: "Quick look",
                    Duration.UNIT: "Detailed review",
                    Duration.JOURNEY: "Checklist use",
                    Duration.CAMPAIGN: "Peer and teacher sign-off"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Data Log Check",
                purpose="Make sure data is recorded neatly and correctly",
                implementation_guidance="Teacher reviews data tables",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "After each data session",
                    Duration.CAMPAIGN: "Weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Spot check",
                    Duration.UNIT: "Basic review",
                    Duration.JOURNEY: "Peer feedback",
                    Duration.CAMPAIGN: "Team review"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Hypothesis Presentation",
                purpose="Share and explain your hypothesis",
                typical_timing="After planning phase",
                assessment_focus=["Clarity", "Testability"],
                rubric_guidance="Assess if hypothesis matches question and is testable"
            ),
            SummativeAssessmentMoment(
                moment_name="Experiment Demo",
                purpose="Show your experiment in action",
                typical_timing="During Do & Observe",
                assessment_focus=["Safety", "Following steps"],
                rubric_guidance="Evaluate safety and procedure accuracy"
            ),
            SummativeAssessmentMoment(
                moment_name="Data Explanation",
                purpose="Explain what your data shows",
                typical_timing="After data collection",
                assessment_focus=["Accuracy", "Patterns identified"],
                rubric_guidance="Assess correctness and insight into results"
            ),
            SummativeAssessmentMoment(
                moment_name="Final Reflection",
                purpose="Reflect on your findings and next steps",
                typical_timing="At project end",
                assessment_focus=["Depth of reflection", "Connection to hypothesis"],
                rubric_guidance="Evaluate insight and future planning"
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="What Surprised Me",
                purpose="Notice unexpected results",
                structure=[
                    "Describe one surprising result",
                    "Explain why it surprised you",
                    "What new question do you have?"
                ],
                timing_guidance="After data analysis",
                facilitation_notes="Use quick write or circle share"
            ),
            ReflectionProtocol(
                protocol_name="Next Experiment",
                purpose="Plan how to improve or explore further",
                structure=[
                    "What would you change?",
                    "Why would that help?",
                    "How will you test it?"
                ],
                timing_guidance="During final reflection",
                facilitation_notes="Discuss in pairs before writing"
            )
        ],
        portfolio_guidance="Keep a lab notebook with your question, hypothesis, notes, data, and reflections."
    ),
    
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teacher",
            "Family members at home",
            "School science fair visitors"
        ],
        engagement_formats=[
            "Class demo",
            "Science fair poster",
            "Short video or slideshow"
        ],
        preparation_requirements=[
            "Practice explaining your steps",
            "Check safety and data accuracy",
            "Make your visuals bright and clear"
        ],
        logistical_considerations=[
            "Reserve demo area",
            "Set presentation time",
            "Invite audience"
        ]
    ),
    
    project_management_tools=[
        "Lab notebook",
        "Materials chart",
        "Procedure checklist",
        "Data recording sheet",
        "Presentation plan"
    ],
    
    recommended_resources=[
        "Simple experiment kits",
        "Child-safe lab tools",
        "Kid-friendly science books",
        "Science videos for kids",
        "Printable data tables"
    ],
    
    technology_suggestions=[
        "Digital timers or stopwatches",
        "Tablet or camera for photos",
        "Basic sensors (e.g., thermometer)",
        "Presentation software"
    ],
    
    standards_alignment_examples={
        "science": [
            "NGSS 3-PS2-1: Plan and conduct an investigation to provide evidence of the effects of balanced and unbalanced forces.",
            "NGSS 4-PS3-2: Make observations to provide evidence that energy can be transferred in various ways."
        ],
        "cross_curricular": [
            "Measurement and data skills",
            "Writing and communication",
            "Collaboration"
        ]
    },
    
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge="Design and carry out a fair test, analyze results, and explain findings.",
        authenticity="Questions come from students’ own curiosities and everyday life.",
        public_product="A lab notebook, demo, and presentation.",
        collaboration="Work in teams to run experiments.",
        project_management="Follow multi-step procedure with checkpoints.",
        reflection="Ongoing thinking about how and why things happen."
    ),
    
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN],
        social_structure_compatible=[SocialStructure.INDIVIDUAL, SocialStructure.COLLABORATIVE],
        cognitive_complexity_range=[CognitiveComplexity.ANALYSIS, CognitiveComplexity.EVALUATION],
        authenticity_compatible=[AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED],
        scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED],
        product_complexity_compatible=[ProductComplexity.PORTFOLIO, ProductComplexity.EXPERIENCE],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.SYNCHRONOUS_REMOTE]
    ),
    
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we already notice about our question?",
            "What have we learned in class that helps?"
        ],
        what_we_wonder_prompts=[
            "What might happen if we change one thing?",
            "Why do we think that will happen?"
        ],
        what_we_want_to_learn_prompts=[
            "How can we test our hypothesis?",
            "What data will help answer our question?"
        ],
        how_we_might_explore_options=[
            "Design a fair test",
            "Observe and record carefully",
            "Repeat the experiment"
        ],
        reflection_return_prompts=[
            "How did our results compare to our guess?",
            "What surprised us most?"
        ]
    ),
    
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Experiment tables with safety gear",
            "Data recording station",
            "Observation corner",
            "Reflection nook"
        ],
        documentation_displays=[
            "Lab notebooks on display",
            "Data charts pinned up",
            "Photos of experiments in action"
        ],
        material_provocations=[
            "Sample materials kits",
            "Experiment examples",
            "Question prompt cards"
        ],
        collaboration_zones=[
            "Partner experiment stations",
            "Group discussion area"
        ],
        reflection_retreats=[
            "Quiet writing spots",
            "Circle-sharing area"
        ]
    ),
    
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Pick your own question to test",
            "Choose variables to change",
            "Decide how to record what happens",
            "Select how to share your findings"
        ],
        voice_amplification_strategies=[
            "Students lead their own experiments",
            "Peers ask each other questions"
        ],
        ownership_transfer_milestones=[
            "Write your own procedure steps",
            "Manage data notebook"
        ],
        peer_collaboration_structures=[
            "Buddy safety checks",
            "Team data discussions"
        ]
    ),
    
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Take photos of each step",
            "Draw diagrams of setup",
            "Record measurements in notebook"
        ],
        student_thinking_artifacts=[
            "Hypothesis sheets",
            "Data tables",
            "Reflection journal pages"
        ],
        process_documentation_methods=[
            "Photo journals",
            "Lab notebook entries"
        ],
        celebration_sharing_formats=[
            "Science fair",
            "Class demo day"
        ]
    ),
    
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Draw step-by-step diagrams",
            "Create a picture story"
        ],
        kinesthetic_expression_options=[
            "Act out what happens",
            "Use movement to show results"
        ],
        verbal_expression_options=[
            "Explain your experiment to friends",
            "Record a mini-podcast"
        ],
        collaborative_expression_options=[
            "Team presentations",
            "Peer interviews"
        ],
        creative_expression_options=[
            "Make a science comic",
            "Compose a short song about your findings"
        ]
    ),
    
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "Experiment fails to work",
            "Data isn’t clear",
            "Safety concerns arise"
        ],
        student_interest_amplifiers=[
            "Offer choice of different materials",
            "Connect experiment to favorite topics"
        ],
        unexpected_connection_bridges=[
            "Link results to everyday examples",
            "Connect to related science topics"
        ],
        community_opportunity_integrators=[
            "Invite a local scientist to visit",
            "Share at a school science fair"
        ]
    ),
    
    getting_started_essentials=[
        "Gather safe, child-friendly materials",
        "Review safety rules together",
        "Set up experiment space"
    ],
    when_things_go_wrong=[
        "Experiment spills: model cleanup",
        "Data errors: repeat trial",
        "Hypothesis too broad: narrow focus"
    ],
    success_indicators=[
        "Questions are clear and testable",
        "Procedures are followed safely",
        "Data is recorded neatly",
        "Conclusions match data",
        "Reflections show new ideas"
    ],
    teacher_preparation_notes=[
        "Prepare experiment kits in advance",
        "Model a sample experiment",
        "Review safety guidelines with students",
        "Have materials organized by station"
    ],
    common_challenges=[
        "Hypotheses are too vague",
        "Steps are skipped or out of order",
        "Data isn’t recorded correctly",
        "Safety rules not followed"
    ],
    teacher_prep_essentials=[
        "Print procedure and data sheets",
        "Gather safety supplies (goggles, aprons)",
        "Arrange workstations with materials"
    ],
    student_readiness="Best for grades 3–7 who can follow simple procedures under supervision.",
    community_engagement_level="Low – activity is classroom-based with optional family demos at home.",
    assessment_highlights=[
        "Clarity and testability of hypothesis",
        "Accuracy of data collection",
        "Safety and procedure adherence",
        "Depth of reflection"
    ],
    assessment_focus="Skills in asking questions, planning and running tests, collecting data, and explaining findings.",
    what_success_looks_like="Students design and carry out a safe experiment, record and interpret data, and share clear conclusions.",
    final_product_description="A lab report or demonstration showing question, procedure, data, and conclusions.",
    
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Scientific Inquiry",
            application="Students formulate questions, plan and run experiments.",
            assessment_connection="Assessed via clarity and safety in procedure and data use."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Data Analysis",
            application="Students record, graph, and interpret their data.",
            assessment_connection="Assessed via accuracy and insight in analysis."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Communication",
            application="Students share their findings clearly and reflect on results.",
            assessment_connection="Assessed via presentation and reflection quality."
        )
    ]
)
