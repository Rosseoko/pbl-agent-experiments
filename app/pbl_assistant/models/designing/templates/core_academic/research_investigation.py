# templates/core_academic/research_investigation.py

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
    AuthenticityLevel, ScaffoldingIntensity, ProductComplexity,
    DeliveryMode, SubjectArea
)

TEMPLATE = create_research_investigation_template = BaseTemplate(
    template_id="research_investigation",
    intent=TemplateIntent.RESEARCH_INVESTIGATION,
    display_name="Research Investigation Project",
    description=(
        "Students learn to think like junior scientists: they ask questions, "
        "plan investigations, gather and analyze data, and share their findings."
    ),
    pedagogical_approach="Inquiry-based learning through hands-on research and experimentation",
    comprehensive_overview=(
        "In this project, students pick a science question they’re curious about—"
        "for example, how plants grow under different lights or which materials float best. "
        "They brainstorm, research background info, form a hypothesis, plan and carry out "
        "an experiment, collect and record results, analyze patterns, and then present "
        "what they learned to others."
    ),
    driving_question_template="How can we investigate [our science question] to find an answer?",
    
    core_learning_cycle=[
        "Ask & Wonder",
        "Background Research",
        "Plan & Experiment",
        "Collect & Analyze Data",
        "Share & Reflect"
    ],
    
    essential_skills=[
        "question_formulation",
        "background_research",
        "hypothesis_development",
        "experiment_planning",
        "data_collection",
        "data_analysis",
        "communication",
        "reflection"
    ],
    
    required_components=[
        "driving_question",
        "research_notes",
        "hypothesis",
        "materials_list",
        "procedure_steps",
        "data_records",
        "analysis_summary",
        "conclusion",
        "reflection_notes"
    ],
    
    natural_subject_areas=[
        SubjectArea.SCIENCE,
        SubjectArea.MATHEMATICS
    ],
    
    cross_curricular_connections=[
        "Reading informational texts",
        "Writing observation notes",
        "Basic measurements and charts",
        "Drawing diagrams",
        "Team discussion and presentation"
    ],
    
    entry_event_framework=EntryEventFramework(
        purpose="Spark curiosity with a simple demo or question",
        design_principles=[
            "Use a vivid hands-on demonstration",
            "Encourage ‘I wonder…’ questions",
            "Connect to students’ experiences",
            "Keep it safe and visible"
        ],
        template_options=[
            EntryEventOption(
                type="mystery_mixture",
                example="Mix baking soda and vinegar and watch it fizz",
                student_response_pattern="Observe → ask questions → discuss",
                question_generation_method="What do you notice? What might change if we…?",
                estimated_time="15 minutes",
                materials_needed=["Baking soda", "Vinegar", "Cups", "Spoons"]
            ),
            EntryEventOption(
                type="plant_growth_demo",
                example="Show two seedlings under different light and ask: Why do they grow differently?",
                student_response_pattern="Observe → record differences → brainstorm ideas",
                question_generation_method="What makes one plant grow faster?",
                estimated_time="10 minutes discussion",
                materials_needed=["Seedlings", "Two light sources", "Chart paper"]
            )
        ],
        customization_guidance="Choose a demo that fits your classroom supplies and student interests"
    ),
    
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Ask & Wonder",
            learning_purpose="Generate clear, testable science questions",
            core_activities=[
                "Brainstorm topics and phenomena",
                "Use question starters (What if…? How does…? Why might…?)",
                "Select one question",
                "Write it down"
            ],
            essential_deliverables=["Written driving question"],
            reflection_checkpoints=[
                "Is our question specific and testable?",
                "What do we expect to learn?"
            ],
            duration_scaling_notes="Sprint: Question only; Unit: Add rationale"
        ),
        MilestoneTemplate(
            milestone_name="Background Research",
            learning_purpose="Gather simple facts and observations before experimenting",
            core_activities=[
                "Read a short article or watch a video",
                "Take notes on key points",
                "Discuss what we learned"
            ],
            essential_deliverables=["Research notes with 3–5 facts"],
            reflection_checkpoints=[
                "What did we learn about our topic?",
                "Which facts help shape our hypothesis?"
            ],
            duration_scaling_notes="Sprint: 1 source; Unit: 2–3 sources; Journey: 4+ sources"
        ),
        MilestoneTemplate(
            milestone_name="Plan & Experiment",
            learning_purpose="Design and conduct a fair test",
            core_activities=[
                "List materials",
                "Write step-by-step procedure",
                "Identify what to change and what to keep the same",
                "Carry out experiment safely"
            ],
            essential_deliverables=[
                "Materials list", "Procedure steps", "Completed experiment"
            ],
            reflection_checkpoints=[
                "Do we have all materials?",
                "Is our procedure clear and safe?"
            ],
            duration_scaling_notes="Sprint: Draft plan; Unit: Execute one trial; Journey: Multiple trials"
        ),
        MilestoneTemplate(
            milestone_name="Collect & Analyze Data",
            learning_purpose="Record results and look for patterns",
            core_activities=[
                "Use tables or charts to record data",
                "Count, measure, or rate results",
                "Create a simple graph or diagram",
                "Discuss what the data show"
            ],
            essential_deliverables=[
                "Filled data chart", "Graph or diagram", "Analysis notes"
            ],
            reflection_checkpoints=[
                "What patterns do we see?",
                "Does the data match our hypothesis?"
            ],
            duration_scaling_notes="Sprint: One chart; Unit: Chart + notes; Journey: Chart, notes + peer discussion"
        ),
        MilestoneTemplate(
            milestone_name="Share & Reflect",
            learning_purpose="Communicate findings and consider next steps",
            core_activities=[
                "Prepare a short presentation or poster",
                "Explain our question, procedure, and results",
                "Write or draw a reflection on what we learned"
            ],
            essential_deliverables=[
                "Presentation slides or poster", "Reflection entry"
            ],
            reflection_checkpoints=[
                "How clear is our explanation?",
                "What would we try next time?"
            ],
            duration_scaling_notes="Same steps; vary depth by duration"
        )
    ],
    
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Question Tracker",
                purpose="Monitor clarity of student questions",
                implementation_guidance="Students update log as they refine questions",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After planning",
                    Duration.JOURNEY: "Weekly",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Simple list",
                    Duration.UNIT: "Labeled chart",
                    Duration.JOURNEY: "Detailed notes",
                    Duration.CAMPAIGN: "Digital log"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Research Notes Check",
                purpose="Ensure students record accurate background info",
                implementation_guidance="Teacher reviews notes mid-project",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "After each source",
                    Duration.CAMPAIGN: "Weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Spot check",
                    Duration.UNIT: "Basic feedback",
                    Duration.JOURNEY: "Peer review",
                    Duration.CAMPAIGN: "Rubric-based"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Procedure & Data Check",
                purpose="Check experiment steps and data recording",
                implementation_guidance="Peers and teacher give feedback on drafts",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "Midway",
                    Duration.JOURNEY: "Bi-monthly",
                    Duration.CAMPAIGN: "Monthly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Peer check",
                    Duration.UNIT: "Teacher review",
                    Duration.JOURNEY: "Expert feedback",
                    Duration.CAMPAIGN: "Community input"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Hypothesis Presentation",
                purpose="Share and explain our hypothesis",
                typical_timing="After planning phase",
                assessment_focus=["Clarity", "Testability"],
                rubric_guidance="Assess if hypothesis is precise and testable"
            ),
            SummativeAssessmentMoment(
                moment_name="Research Report",
                purpose="Present background findings and plan",
                typical_timing="After research phase",
                assessment_focus=["Use of sources", "Organization"],
                rubric_guidance="Evaluate accuracy and structure of notes"
            ),
            SummativeAssessmentMoment(
                moment_name="Data & Analysis Share",
                purpose="Show data and explain patterns",
                typical_timing="After data analysis",
                assessment_focus=["Accuracy", "Insight"],
                rubric_guidance="Assess correctness and interpretation"
            ),
            SummativeAssessmentMoment(
                moment_name="Final Reflection",
                purpose="Reflect on our investigation and future questions",
                typical_timing="Project end",
                assessment_focus=["Depth", "Connection to learning"],
                rubric_guidance="Evaluate insight and planning for next steps"
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="What Surprised Me",
                purpose="Notice unexpected results or facts",
                structure=[
                    "Describe one surprise",
                    "Explain why it surprised you",
                    "What question does it raise now?"
                ],
                timing_guidance="After data analysis",
                facilitation_notes="Use exit tickets or circle share"
            ),
            ReflectionProtocol(
                protocol_name="Next Investigation",
                purpose="Plan how to explore further",
                structure=[
                    "What would we change?",
                    "Why would that help?",
                    "How will we test it?"
                ],
                timing_guidance="During final reflection",
                facilitation_notes="Discuss with a partner first"
            )
        ],
        portfolio_guidance=(
            "Keep all questions, notes, data charts, analyses, and reflections in one folder or notebook."
        )
    ),
    
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teacher",
            "Family members at home",
            "School science fair visitors"
        ],
        engagement_formats=[
            "Poster session",
            "Short class demo",
            "Digital slideshow"
        ],
        preparation_requirements=[
            "Practice your talk",
            "Check your data and visuals",
            "Make it clear and colorful"
        ],
        logistical_considerations=[
            "Reserve a display area",
            "Schedule presentation time",
            "Invite viewers"
        ]
    ),
    
    project_management_tools=[
        "Question log chart",
        "Research notes binder",
        "Materials checklist",
        "Procedure worksheet",
        "Presentation planner"
    ],
    
    recommended_resources=[
        "Child-friendly science books",
        "Simple experiment kits",
        "Library or online articles",
        "YouTube science demos for kids",
        "Printable data tables"
    ],
    
    technology_suggestions=[
        "Tablet or computer for research",
        "Digital timers or sensors",
        "Graphing apps",
        "Presentation software"
    ],
    
    standards_alignment_examples={
        "science": [
            "NGSS 3-ESS2-1: Represent data in tables and graphical displays to describe typical weather conditions.",
            "NGSS 4-PS3-2: Make observations to provide evidence that energy can be transferred."
        ],
        "cross_curricular": [
            "Research and inquiry skills",
            "Data literacy",
            "Communication skills"
        ]
    },
    
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge=(
            "Students design and conduct a real investigation, analyze data, and draw conclusions."
        ),
        authenticity="Questions are student-generated and investigations use real materials.",
        public_product="A report, poster, or slideshow sharing their findings.",
        collaboration="Work in pairs or small teams to investigate and share.",
        project_management="Plan, execute, and reflect in a clear sequence.",
        reflection="Ongoing thinking about what data tells us and what to explore next."
    ),
    
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN],
        social_structure_compatible=[SocialStructure.INDIVIDUAL, SocialStructure.COLLABORATIVE],
        cognitive_complexity_range=[CognitiveComplexity.ANALYSIS, CognitiveComplexity.EVALUATION],
        authenticity_compatible=[AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED],
        scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED],
        product_complexity_compatible=[ProductComplexity.PORTFOLIO, ProductComplexity.SYSTEM],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.SYNCHRONOUS_REMOTE]
    ),
    
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we already know about our topic?",
            "What have we learned from our background research?"
        ],
        what_we_wonder_prompts=[
            "What happens if we change one thing?",
            "Why do we think that will happen?"
        ],
        what_we_want_to_learn_prompts=[
            "What data will help us answer our question?",
            "How can we make our investigation fair?"
        ],
        how_we_might_explore_options=[
            "Plan an experiment or survey",
            "Use videos or books to learn more",
            "Collect measurements carefully"
        ],
        reflection_return_prompts=[
            "How did our understanding change?",
            "What new questions do we have?"
        ]
    ),
    
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Investigation tables with supplies",
            "Data recording station",
            "Reflection corner with journals"
        ],
        documentation_displays=[
            "Question charts",
            "Research notes on display",
            "Data graphs pinned up"
        ],
        material_provocations=[
            "Sample experiments setup",
            "Research prompt cards"
        ],
        collaboration_zones=[
            "Partner workstations",
            "Group discussion area"
        ],
        reflection_retreats=[
            "Quiet writing nook",
            "Circle share area"
        ]
    ),
    
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Choose a question to investigate",
            "Select sources or materials",
            "Decide how to record data",
            "Pick a format to share findings"
        ],
        voice_amplification_strategies=[
            "Students lead their own investigations",
            "Peer feedback sessions"
        ],
        ownership_transfer_milestones=[
            "Write and refine investigation plans",
            "Manage research notebook"
        ],
        peer_collaboration_structures=[
            "Buddy checks for accuracy",
            "Team analysis discussions"
        ]
    ),
    
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Photo journeys of experiments",
            "Notebook entries of each step",
            "Graph drafts"
        ],
        student_thinking_artifacts=[
            "Question lists",
            "Research notes",
            "Data tables"
        ],
        process_documentation_methods=[
            "Binder or digital folder",
            "Photo journals"
        ],
        celebration_sharing_formats=[
            "Class showcase",
            "Poster walk"
        ]
    ),
    
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Draw diagrams or charts",
            "Build simple models"
        ],
        kinesthetic_expression_options=[
            "Act out an experiment",
            "Use movement to show patterns"
        ],
        verbal_expression_options=[
            "Tell the story of your investigation",
            "Record a mini-podcast"
        ],
        collaborative_expression_options=[
            "Team presentations",
            "Peer interviews"
        ],
        creative_expression_options=[
            "Write a short research journal",
            "Create a comic strip of your steps"
        ]
    ),
    
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "Unexpected results",
            "Missing materials",
            "Data doesn’t match hypothesis"
        ],
        student_interest_amplifiers=[
            "Offer choice of topics",
            "Connect to real-life examples"
        ],
        unexpected_connection_bridges=[
            "Link findings to art or math",
            "Compare with everyday objects"
        ],
        community_opportunity_integrators=[
            "Invite a local scientist visitor",
            "Share results at family science night"
        ]
    ),
    
    getting_started_essentials=[
        "Gather safe, child-friendly supplies",
        "Review safety and notes templates",
        "Set up investigation stations"
    ],
    when_things_go_wrong=[
        "Experiment fails: model cleanup and repeat",
        "Notes missing: guide note-taking",
        "Hypothesis unclear: refine question"
    ],
    success_indicators=[
        "Questions are clear and focused",
        "Research notes are complete",
        "Data charts show patterns",
        "Presentations are engaging",
        "Reflections show new insights"
    ],
    teacher_preparation_notes=[
        "Prepare investigation kits in advance",
        "Model note-taking and data collection",
        "Arrange materials by station",
        "Review safety and procedure guidelines"
    ],
    common_challenges=[
        "Questions too broad or vague",
        "Difficulty recording data consistently",
        "Overlooking reflection step",
        "Presentation anxiety"
    ],
    teacher_prep_essentials=[
        "Print investigation and data sheets",
        "Organize materials and safety gear",
        "Plan a sample demonstration"
    ],
    student_readiness="Ideal for grades 3–7 who can follow simple procedures with guidance.",
    community_engagement_level="Low – primarily classroom-based with optional family sharing.",
    assessment_highlights=[
        "Clarity of questions",
        "Quality of research notes",
        "Accuracy of data collection",
        "Depth of analysis",
        "Effectiveness of presentation"
    ],
    assessment_focus="Skills in asking questions, researching, experimenting, analyzing, and communicating.",
    what_success_looks_like="Students complete a full investigation cycle and explain their findings confidently.",
    final_product_description=(
        "A research report or poster showing question, background, data, analysis, and reflections."
    ),
    
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Scientific Inquiry",
            application="Students plan and carry out investigations.",
            assessment_connection="Assessed via clarity and rigor of their inquiry."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Data Literacy",
            application="Students collect, chart, and interpret data.",
            assessment_connection="Assessed via accuracy and insight in analysis."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Communication",
            application="Students share their process and findings clearly.",
            assessment_connection="Assessed via presentation and reflection quality."
        )
    ]
)
