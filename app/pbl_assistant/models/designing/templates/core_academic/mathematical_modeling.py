# templates/core_academic/mathematical_modeling.py

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

TEMPLATE = create_mathematical_modeling_template = BaseTemplate(
    template_id="mathematical_modeling",
    intent=TemplateIntent.MATHEMATICAL_MODELING,
    display_name="Mathematical Modeling Project",
    description=(
        "Students use math to understand and solve real-world problems by creating, testing, "
        "and refining simple models like charts, equations, or diagrams."
    ),
    pedagogical_approach="Hands-on inquiry through data collection and model building",
    comprehensive_overview=(
        "In this project, students pick a question—like how many cups of juice we need for a party "
        "or how fast a plant grows over days. They learn to collect data, build a math model (a chart, "
        "equation, or diagram), test their predictions, improve the model, and share what they discover. "
        "Along the way, they practice measuring, graphing, critical thinking, and teamwork."
    ),
    driving_question_template="How can we use math to [solve or explore a problem] in our world?",
    
    core_learning_cycle=[
        "Ask & Plan",
        "Gather Data",
        "Build Model",
        "Test & Refine",
        "Share & Reflect"
    ],
    
    essential_skills=[
        "question_formulation",
        "data_collection",
        "model_construction",
        "data_analysis",
        "iteration",
        "presentation",
        "reflection"
    ],
    
    required_components=[
        "driving_question",
        "data_sheet",
        "initial_model",
        "test_results",
        "refined_model",
        "reflection_notes"
    ],
    
    natural_subject_areas=[
        SubjectArea.MATHEMATICS,
        SubjectArea.SCIENCE
    ],
    
    cross_curricular_connections=[
        "Reading and interpreting data tables",
        "Writing lab-style reports",
        "Art and design for clear visuals",
        "Basic computing for charts",
        "Teamwork and communication"
    ],
    
    entry_event_framework=EntryEventFramework(
        purpose="Get students excited about using math for real questions",
        design_principles=[
            "Connect to everyday situations",
            "Use concrete objects or images",
            "Encourage ‘I wonder…’ questions",
            "Keep it playful and visual"
        ],
        template_options=[
            EntryEventOption(
                type="party_budget_challenge",
                example="Show pictures of party supplies with prices; ask how many to buy with a set budget",
                student_response_pattern="Observe → ask questions → estimate with play money",
                question_generation_method="What would you like to know? How many items can we afford?",
                estimated_time="30 minutes",
                materials_needed=["Play money", "Pictures or cards of supplies", "Price list"]
            ),
            EntryEventOption(
                type="measurement_mystery",
                example="Measure footprints in the playground and guess who made them by size patterns",
                student_response_pattern="Measure → record → compare",
                question_generation_method="What does the data tell us? How can we predict the maker?",
                estimated_time="30 minutes",
                materials_needed=["Measuring tapes", "Worksheet", "Clipboards"]
            )
        ],
        customization_guidance="Pick an entry event that fits your class space and interests"
    ),
    
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Ask & Plan",
            learning_purpose="Define a clear math question and plan how to collect data",
            core_activities=[
                "Brainstorm real-world problems",
                "Use question starters (How many? How much? How fast?)",
                "Choose one question and list needed information",
                "Plan data collection steps"
            ],
            essential_deliverables=[
                "Written driving question",
                "Data collection plan"
            ],
            reflection_checkpoints=[
                "Is our question clear?",
                "What data do we need?",
                "How will we gather it?"
            ],
            duration_scaling_notes="Sprint: Question only; Unit: Add plan; Journey: Start data collection"
        ),
        MilestoneTemplate(
            milestone_name="Gather Data",
            learning_purpose="Collect accurate measurements or survey results",
            core_activities=[
                "Use tools (ruler, scale, survey)",
                "Record data carefully in tables",
                "Check for mistakes with a partner"
            ],
            essential_deliverables=[
                "Completed data sheet with at least 5 entries"
            ],
            reflection_checkpoints=[
                "Is our data accurate?",
                "What patterns do we see?",
                "Do we need more data?"
            ],
            duration_scaling_notes="Sprint: 5 entries; Unit: 10 entries; Journey: 15+ entries"
        ),
        MilestoneTemplate(
            milestone_name="Build Model",
            learning_purpose="Create a simple math model to represent the data",
            core_activities=[
                "Choose a representation (graph, chart, equation)",
                "Plot or calculate initial model",
                "Label all parts clearly"
            ],
            essential_deliverables=[
                "Draft model (bar graph, line plot, or equation)"
            ],
            reflection_checkpoints=[
                "Does our model match the data?",
                "Is it easy to read?",
                "What questions remain?"
            ],
            duration_scaling_notes="Sprint: Quick sketch; Unit: Neat chart; Journey: Digital graph"
        ),
        MilestoneTemplate(
            milestone_name="Test & Refine",
            learning_purpose="Use the model to make predictions and improve accuracy",
            core_activities=[
                "Predict a new data point",
                "Collect new data to test",
                "Adjust model as needed"
            ],
            essential_deliverables=[
                "Prediction record",
                "Test results",
                "Revised model"
            ],
            reflection_checkpoints=[
                "How close was our prediction?",
                "What changes help our model fit better?",
                "What did we learn?"
            ],
            duration_scaling_notes="Sprint: One test; Unit: Two tests; Journey: Multiple iterations"
        ),
        MilestoneTemplate(
            milestone_name="Share & Reflect",
            learning_purpose="Present findings and think about real-world uses",
            core_activities=[
                "Prepare short presentation or poster",
                "Explain model and results",
                "Write a reflection on lessons learned"
            ],
            essential_deliverables=[
                "Presentation or poster",
                "Reflection journal"
            ],
            reflection_checkpoints=[
                "How well did our model work?",
                "Where could we use this in real life?",
                "What would we try next time?"
            ],
            duration_scaling_notes="Same steps; vary depth by duration"
        )
    ],
    
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Question Tracker",
                purpose="Monitor clarity of driving questions",
                implementation_guidance="Students update question log as they refine it",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After planning",
                    Duration.JOURNEY: "Weekly",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Simple list",
                    Duration.UNIT: "Organized chart",
                    Duration.JOURNEY: "Detailed journal",
                    Duration.CAMPAIGN: "Digital portfolio"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Data Journal Check",
                purpose="Ensure data collection is accurate and complete",
                implementation_guidance="Teacher reviews data sheets mid-project",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "After each data session",
                    Duration.CAMPAIGN: "Weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Spot check",
                    Duration.UNIT: "Basic review",
                    Duration.JOURNEY: "Detailed feedback",
                    Duration.CAMPAIGN: "Peer review"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Model Draft Review",
                purpose="Check the initial model for accuracy and clarity",
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
                    Duration.JOURNEY: "Expert input",
                    Duration.CAMPAIGN: "Community feedback"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Data Report",
                purpose="Show collected data clearly",
                typical_timing="After gathering data",
                assessment_focus=["Completeness", "Accuracy"],
                rubric_guidance="Assess table layout and correctness"
            ),
            SummativeAssessmentMoment(
                moment_name="Model Presentation",
                purpose="Explain the draft model and interpretation",
                typical_timing="After building model",
                assessment_focus=["Clarity", "Data match"],
                rubric_guidance="Evaluate labeling and explanation"
            ),
            SummativeAssessmentMoment(
                moment_name="Final Model & Results",
                purpose="Share refined model and findings",
                typical_timing="Project conclusion",
                assessment_focus=["Improvement", "Insight"],
                rubric_guidance="Assess how well revisions improved fit"
            ),
            SummativeAssessmentMoment(
                moment_name="Reflection Write-Up",
                purpose="Reflect on what worked and next steps",
                typical_timing="After presentations",
                assessment_focus=["Depth", "Connection to real life"],
                rubric_guidance="Evaluate insight and application"
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="What Worked?",
                purpose="Identify strengths of our model",
                structure=[
                    "Name one thing that worked well",
                    "Explain why it worked",
                    "What made it possible?"
                ],
                timing_guidance="After testing",
                facilitation_notes="Use exit tickets or quick shares"
            ),
            ReflectionProtocol(
                protocol_name="Next Steps",
                purpose="Plan how to improve or use the model further",
                structure=[
                    "What would we change?",
                    "How could we test again?",
                    "Where else could we use this?"
                ],
                timing_guidance="After sharing",
                facilitation_notes="Discuss in pairs before writing"
            )
        ],
        portfolio_guidance=(
            "Keep all data sheets, model drafts, test results, and reflections in one folder."
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
            "Short classroom demo",
            "Digital slideshow"
        ],
        preparation_requirements=[
            "Practice explaining predictions",
            "Check labels and data accuracy",
            "Make visuals clear and colorful"
        ],
        logistical_considerations=[
            "Reserve display boards or screen",
            "Set a time for presentations",
            "Invite viewers"
        ]
    ),
    
    project_management_tools=[
        "Question log chart",
        "Data collection tracker",
        "Model planning sheet",
        "Draft feedback checklist",
        "Presentation rehearsal guide"
    ],
    
    recommended_resources=[
        "Rulers, scales, timers",
        "Graph paper or grid notebooks",
        "Simple calculators",
        "Chart-making apps or printables",
        "Books on data and patterns"
    ],
    
    technology_suggestions=[
        "Spreadsheet software (e.g., Sheets)",
        "Tablet for data entry",
        "Simple sensors (e.g., temperature probe)",
        "Graphing tools online"
    ],
    
    standards_alignment_examples={
        "mathematics": [
            "CCSS.MATH.CONTENT.3.MD.A.1: Tell and write time to the nearest minute and measure intervals of time.",
            "CCSS.MATH.CONTENT.4.MD.B.4: Make a line plot to display a data set of measurements in fractions.",
            "CCSS.MATH.CONTENT.5.OA.A.2: Write simple expressions that record calculations with numbers."
        ],
        "cross_curricular": [
            "Data literacy and interpretation",
            "Scientific inquiry skills",
            "Computational thinking"
        ]
    },
    
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge=(
            "Students define a problem, collect and analyze real data, and build working models."
        ),
        authenticity="Models answer real questions from students’ lives.",
        public_product="A working model display with data and explanations.",
        collaboration="Work in teams to collect data and build models.",
        project_management="Clear plan with milestones for data and modeling.",
        reflection="Regular check-ins on model accuracy and next steps."
    ),
    
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN],
        social_structure_compatible=[SocialStructure.INDIVIDUAL, SocialStructure.COLLABORATIVE],
        cognitive_complexity_range=[CognitiveComplexity.ANALYSIS, CognitiveComplexity.SYNTHESIS],
        authenticity_compatible=[AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED],
        scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED],
        product_complexity_compatible=[ProductComplexity.SYSTEM, ProductComplexity.PORTFOLIO],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.SYNCHRONOUS_REMOTE]
    ),
    
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we already know about our question?",
            "What examples can we recall from everyday life?"
        ],
        what_we_wonder_prompts=[
            "How many? How much? How fast? How often?",
            "What patterns or relationships might we find?"
        ],
        what_we_want_to_learn_prompts=[
            "Which model will predict best?",
            "How can we use data to improve our ideas?"
        ],
        how_we_might_explore_options=[
            "Measure and record results",
            "Survey friends or family",
            "Watch a demonstration video"
        ],
        reflection_return_prompts=[
            "How did our understanding change?",
            "What surprised us most?"
        ]
    ),
    
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Data corner with clipboards and tables",
            "Chart wall for posting graphs",
            "Model-building station with supplies",
            "Reflection nook with journals"
        ],
        documentation_displays=[
            "Data sheets pinned up",
            "Model drafts on a board",
            "Reflection notes displayed"
        ],
        material_provocations=[
            "Measuring tools (rulers, timers)",
            "Sample data sets",
            "Pictures of real models"
        ],
        collaboration_zones=[
            "Partner tables for data collection",
            "Group graphing area"
        ],
        reflection_retreats=[
            "Quiet writing space",
            "Think-pair-share corners"
        ]
    ),
    
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Choose which problem to model",
            "Select measurement tools",
            "Decide model format (chart, equation)",
            "Pick presentation style"
        ],
        voice_amplification_strategies=[
            "Students lead data talks",
            "Peer feedback on models"
        ],
        ownership_transfer_milestones=[
            "Design own data sheets",
            "Plan model revisions"
        ],
        peer_collaboration_structures=[
            "Buddy data-check",
            "Team model brainstorming"
        ]
    ),
    
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Photo-document data collection",
            "Record model-building steps",
            "Save draft and final models"
        ],
        student_thinking_artifacts=[
            "Data tables",
            "Model sketches",
            "Prediction logs"
        ],
        process_documentation_methods=[
            "Notebook entries with dates",
            "Photo journal"
        ],
        celebration_sharing_formats=[
            "Class graph gallery",
            "Model expo"
        ]
    ),
    
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Draw bar or line graphs",
            "Build a paper model",
            "Create a chart poster"
        ],
        kinesthetic_expression_options=[
            "Act out data patterns",
            "Use movement to show change"
        ],
        verbal_expression_options=[
            "Explain your model to a friend",
            "Record a mini-report"
        ],
        collaborative_expression_options=[
            "Team presentation",
            "Peer-review stations"
        ],
        creative_expression_options=[
            "Compose a song or rap about your data",
            "Make a short 'how-to' video"
        ]
    ),
    
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "Unexpected data trends",
            "Tool difficulties",
            "Model doesn’t fit new data"
        ],
        student_interest_amplifiers=[
            "Offer extra challenges",
            "Relate data to favorite topics"
        ],
        unexpected_connection_bridges=[
            "Link patterns to art or music",
            "Connect to science experiments"
        ],
        community_opportunity_integrators=[
            "Invite a local engineer or data scientist",
            "Share at a school showcase"
        ]
    ),
    
    getting_started_essentials=[
        "Pick a simple, real problem to model",
        "Gather measuring and recording tools",
        "Set up a data table area"
    ],
    when_things_go_wrong=[
        "Data is messy: show a clear example",
        "Model is confusing: model one together",
        "Math errors: use peer checks"
    ],
    success_indicators=[
        "Students ask clear, measurable questions",
        "Data is accurate and neatly recorded",
        "Models reflect the data well",
        "Presentations show understanding"
    ],
    teacher_preparation_notes=[
        "Prepare data collection templates",
        "Gather measuring tools in advance",
        "Model the process with an example"
    ],
    common_challenges=[
        "Difficulty recording consistent data",
        "Overcomplicating the model",
        "Misreading graphs or charts"
    ],
    teacher_prep_essentials=[
        "Print blank data sheets and graph paper",
        "Organize tools by station",
        "Plan a demonstration example"
    ],
    student_readiness="Works best for students in grades 3–7 who can measure and chart with guidance.",
    community_engagement_level="Low – most work happens in class with possible family sharing.",
    assessment_highlights=[
        "Accuracy of data collection",
        "Effectiveness of the model",
        "Clarity of presentation"
    ],
    assessment_focus="Skills in asking questions, collecting data, building and refining models, and explaining results.",
    what_success_looks_like="Students create a working model that makes accurate predictions and explain it clearly to others.",
    final_product_description="A math model (graph, chart, or equation) with data and a short presentation or poster.",
    
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Problem Formulation",
            application="Students define clear, measurable questions.",
            assessment_connection="Assessed via clarity and focus of questions."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Data Analysis & Modeling",
            application="Students collect data and build accurate models.",
            assessment_connection="Assessed via model accuracy and data use."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Communication & Collaboration",
            application="Students present findings and work with peers.",
            assessment_connection="Assessed via presentation clarity and teamwork."
        )
    ]
)
