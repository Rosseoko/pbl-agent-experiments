# templates/integration_skill/design_thinking.py

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

TEMPLATE = create_design_thinking_template = BaseTemplate(
    template_id="design_thinking",
    intent=TemplateIntent.DESIGN_THINKING,
    display_name="Design Thinking Project",
    description=(
        "Students act like young designers: they notice a problem, imagine solutions, "
        "make a model, test it, and improve their ideas."
    ),
    pedagogical_approach="Human-centered, creative problem solving through iterative design",
    comprehensive_overview=(
        "In this project, students pick something they want to make or improve—like "
        "a friendship bracelet that fits all wrists or a crayon holder that keeps crayons neat. "
        "They learn to notice user needs, brainstorm ideas, build quick prototypes, try them out, "
        "get feedback, and make them better. Along the way, they practice creativity, teamwork, "
        "fine motor skills, and telling stories about their designs."
    ),
    driving_question_template="How might we design [product or solution] that does [user need]?",

    core_learning_cycle=[
        "Empathize & Define",
        "Ideate & Sketch",
        "Prototype & Build",
        "Test & Gather Feedback",
        "Iterate & Reflect"
    ],

    essential_skills=[
        "empathy_and_research",
        "creative_ideation",
        "sketching",
        "model_building",
        "feedback_listening",
        "iteration",
        "presentation",
        "reflection"
    ],

    required_components=[
        "design_brief",
        "user_research_notes",
        "idea_sketches",
        "prototype",
        "test_feedback",
        "iteration_plan",
        "final_design",
        "reflection_notes"
    ],

    natural_subject_areas=[
        SubjectArea.ART,
        SubjectArea.ENGINEERING,
        SubjectArea.SCIENCE
    ],

    cross_curricular_connections=[
        "Art skills for drawing and modeling",
        "Writing clear design briefs",
        "Basic measurement and math for dimensions",
        "Collaboration and communication",
        "Simple science concepts where relevant"
    ],

    entry_event_framework=EntryEventFramework(
        purpose="Help students notice problems and feel curious to solve them",
        design_principles=[
            "Use relatable examples",
            "Encourage observation of user needs",
            "Ask open-ended ‘How might we…?’ questions",
            "Keep it hands-on and playful"
        ],
        template_options=[
            EntryEventOption(
                type="problem_walk",
                example="Take a walk around the classroom or playground, note things that could be easier or more fun",
                student_response_pattern="Observe → note problems → share with partner",
                question_generation_method="What problems did you notice? Who has that problem?",
                estimated_time="20 minutes",
                materials_needed=["Clipboards", "Sticky notes", "Pencils"]
            ),
            EntryEventOption(
                type="show_and_tell_challenge",
                example="Show a common item (e.g., pencil) and ask: How could this be improved?",
                student_response_pattern="Discuss → list ideas → vote favorite",
                question_generation_method="What works well? What could be better?",
                estimated_time="15 minutes",
                materials_needed=["Item to improve", "Chart paper", "Markers"]
            )
        ],
        customization_guidance="Choose an entry event that highlights user empathy and sparks ideas"
    ),

    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Empathize & Define",
            learning_purpose="Understand who you’re designing for and what they need",
            core_activities=[
                "Interview or observe users (classmates or family)",
                "Take notes on needs and problems",
                "Write a simple design brief: user, need, goal"
            ],
            essential_deliverables=[
                "User research notes",
                "Design brief statement"
            ],
            reflection_checkpoints=[
                "Who are we designing for?",
                "What problem are we solving?",
                "Why does it matter?"
            ],
            duration_scaling_notes="Sprint: Observe one user; Unit: Interview 2–3; Journey: Survey a group"
        ),
        MilestoneTemplate(
            milestone_name="Ideate & Sketch",
            learning_purpose="Generate many ideas without judging and draw your favorites",
            core_activities=[
                "Brainstorm as many ideas as possible",
                "Use sticky notes or mind map",
                "Pick top 3 ideas and sketch each"
            ],
            essential_deliverables=[
                "Idea list",
                "3+ sketches"
            ],
            reflection_checkpoints=[
                "Which idea feels most exciting?",
                "What makes it special?"
            ],
            duration_scaling_notes="Sprint: 2 ideas; Unit: 4–5; Journey: 6+"
        ),
        MilestoneTemplate(
            milestone_name="Prototype & Build",
            learning_purpose="Make a quick, simple model of your best idea",
            core_activities=[
                "Choose materials (paper, clay, blocks)",
                "Create a rough prototype",
                "Label key features"
            ],
            essential_deliverables=[
                "Physical or digital prototype"
            ],
            reflection_checkpoints=[
                "What works well in our prototype?",
                "What is too big, small, or hard to use?"
            ],
            duration_scaling_notes="Sprint: Quick paper model; Unit: Basic craft prototype; Journey: Functional model"
        ),
        MilestoneTemplate(
            milestone_name="Test & Gather Feedback",
            learning_purpose="Let users try your prototype and tell you what they think",
            core_activities=[
                "Invite classmates or family to test",
                "Observe how they use it",
                "Ask specific feedback questions"
            ],
            essential_deliverables=[
                "Feedback notes",
                "Observation sketches or photos"
            ],
            reflection_checkpoints=[
                "What surprised you in testing?",
                "Which suggestions help most?"
            ],
            duration_scaling_notes="Same steps; vary number of testers by duration"
        ),
        MilestoneTemplate(
            milestone_name="Iterate & Reflect",
            learning_purpose="Improve your design based on feedback and think about what you learned",
            core_activities=[
                "Plan changes to prototype",
                "Make a revised version",
                "Write a reflection on process and outcome"
            ],
            essential_deliverables=[
                "Iteration plan",
                "Final prototype",
                "Reflection journal"
            ],
            reflection_checkpoints=[
                "How did our design improve?",
                "What would we do next time?"
            ],
            duration_scaling_notes="Sprint: Minor tweaks; Unit: New prototype; Journey: Multiple versions"
        )
    ],

    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Research Check",
                purpose="Ensure students gather relevant user information",
                implementation_guidance="Teacher reviews research notes",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After research",
                    Duration.JOURNEY: "Weekly",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Spot check",
                    Duration.UNIT: "Basic feedback",
                    Duration.JOURNEY: "Peer and teacher feedback",
                    Duration.CAMPAIGN: "Detailed rubric"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Sketch Review",
                purpose="Check clarity and variety in idea sketches",
                implementation_guidance="Peers review sketches with simple criteria",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "After sketching",
                    Duration.CAMPAIGN: "Weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Thumbs up/down",
                    Duration.UNIT: "Verbal comments",
                    Duration.JOURNEY: "Written notes",
                    Duration.CAMPAIGN: "Rubric-based peer review"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Prototype Feedback Check",
                purpose="Capture key insights from prototype testing",
                implementation_guidance="Students use a feedback form",
                frequency_recommendations={
                    Duration.SPRINT: "After first test",
                    Duration.UNIT: "Each test session",
                    Duration.JOURNEY: "After each feedback round",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Simple notes",
                    Duration.UNIT: "Structured form",
                    Duration.JOURNEY: "Peer and teacher input",
                    Duration.CAMPAIGN: "Community feedback"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Design Brief Presentation",
                purpose="Share your problem definition and user needs",
                typical_timing="After empathize phase",
                assessment_focus=["Clarity", "User understanding"],
                rubric_guidance="Assess how well students captured user needs"
            ),
            SummativeAssessmentMoment(
                moment_name="Idea Sketch Share",
                purpose="Present your best ideas and explain choices",
                typical_timing="After sketching phase",
                assessment_focus=["Creativity", "Reasoning"],
                rubric_guidance="Evaluate originality and rationale"
            ),
            SummativeAssessmentMoment(
                moment_name="Prototype Demo",
                purpose="Show and explain your working prototype",
                typical_timing="After building phase",
                assessment_focus=["Functionality", "Label clarity"],
                rubric_guidance="Assess how well prototype meets design brief"
            ),
            SummativeAssessmentMoment(
                moment_name="Final Reflection",
                purpose="Reflect on your design process and learning",
                typical_timing="After iteration phase",
                assessment_focus=["Depth", "Connection to user feedback"],
                rubric_guidance="Evaluate insight and next-step planning"
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="I Like / I Wish",
                purpose="Share positive feedback and suggestions",
                structure=[
                    "I like…",
                    "I wish…"
                ],
                timing_guidance="After testing",
                facilitation_notes="Use sentence stems and modeling"
            ),
            ReflectionProtocol(
                protocol_name="Rose / Thorn / Bud",
                purpose="Identify strengths, challenges, and new ideas",
                structure=[
                    "Rose (strength)",
                    "Thorn (challenge)",
                    "Bud (new idea)"
                ],
                timing_guidance="During final reflection",
                facilitation_notes="Use a chart to record responses"
            )
        ],
        portfolio_guidance=(
            "Keep your research notes, sketches, prototypes, feedback forms, "
            "and reflections in one design folder."
        )
    ),

    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teacher",
            "Family members at home",
            "Other classes"
        ],
        engagement_formats=[
            "Design expo display",
            "Show-and-tell presentation",
            "Photo story sequence"
        ],
        preparation_requirements=[
            "Practice explaining your design choices",
            "Prepare visuals and prototypes",
            "Check workspace layout"
        ],
        logistical_considerations=[
            "Set up tables or display boards",
            "Schedule expo time",
            "Invite audience"
        ]
    ),

    project_management_tools=[
        "User research chart",
        "Idea sketch pads",
        "Prototype materials list",
        "Feedback form",
        "Iteration checklist"
    ],

    recommended_resources=[
        "Paper, cardboard, clay",
        "Basic craft tools (scissors, tape)",
        "Drawing supplies",
        "Kid-friendly design thinking videos",
        "Example prototype galleries"
    ],

    technology_suggestions=[
        "Tablet or computer for digital sketches",
        "Camera for documenting prototypes",
        "Simple modeling software (optional)"
    ],

    standards_alignment_examples={
        "engineering": [
            "NGSS K-2-ETS1-1: Ask questions, make observations, and gather information about a situation people want to change.",
            "NGSS K-2-ETS1-2: Develop a simple sketch, drawing, or physical model to illustrate how the shape of an object helps it function."
        ],
        "art": [
            "21st Century Visual Arts Standard VA:Cr1.1.K-2: Engage collaboratively in creative art-making."
        ],
        "cross_curricular": [
            "Empathy and interviewing skills",
            "Visual communication",
            "Iterative problem solving"
        ]
    },

    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge=(
            "Students empathize, ideate, and prototype solutions to real problems."
        ),
        authenticity="Design challenges come from students’ own experiences.",
        public_product="A prototype and display that communicates the design story.",
        collaboration="Work in teams through every design stage.",
        project_management="Clear steps with research, prototyping, testing, and iteration.",
        reflection="Ongoing reflection on user needs and design improvements."
    ),

    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN],
        social_structure_compatible=[SocialStructure.COLLABORATIVE, SocialStructure.NETWORKED],
        cognitive_complexity_range=[CognitiveComplexity.ANALYSIS, CognitiveComplexity.EVALUATION, CognitiveComplexity.SYNTHESIS],
        authenticity_compatible=[AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED],
        scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED],
        product_complexity_compatible=[ProductComplexity.EXPERIENCE, ProductComplexity.SYSTEM],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.HYBRID, DeliveryMode.SYNCHRONOUS_REMOTE]
    ),

    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What problems do we notice around us?",
            "What do our users need most?"
        ],
        what_we_wonder_prompts=[
            "How might we make this easier or more fun?",
            "What would help people most?"
        ],
        what_we_want_to_learn_prompts=[
            "What do users say about this problem?",
            "What materials or features could work?"
        ],
        how_we_might_explore_options=[
            "Interview users or classmates",
            "Look at similar products online",
            "Sketch and share quick ideas"
        ],
        reflection_return_prompts=[
            "How did our ideas change after testing?",
            "What surprised us about user feedback?"
        ]
    ),

    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Empathy corner with user artifacts",
            "Sketching tables with supplies",
            "Prototype station with varied materials",
            "Feedback wall for sticky notes"
        ],
        documentation_displays=[
            "Design briefs on display",
            "Idea sketches gallery",
            "Prototype photo timeline"
        ],
        material_provocations=[
            "Random craft materials",
            "Example design tools",
            "User persona cards"
        ],
        collaboration_zones=[
            "Team research area",
            "Group sketching space",
            "Feedback discussion circle"
        ],
        reflection_retreats=[
            "Quiet journaling nook",
            "Think-pair-share corners"
        ]
    ),

    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Choose a problem you care about",
            "Decide how to do your research",
            "Pick materials for prototypes",
            "Select who testing participants will be"
        ],
        voice_amplification_strategies=[
            "Students lead user interviews",
            "Peer feedback sessions"
        ],
        ownership_transfer_milestones=[
            "Write and refine own design briefs",
            "Manage prototype iterations"
        ],
        peer_collaboration_structures=[
            "Buddy sketch critiques",
            "Team testing roles"
        ]
    ),

    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Photos of user interviews",
            "Sketch snapshots",
            "Prototype build videos"
        ],
        student_thinking_artifacts=[
            "Design briefs",
            "Sketch notebooks",
            "Feedback forms"
        ],
        process_documentation_methods=[
            "Digital photo journal",
            "Design folder or binder"
        ],
        celebration_sharing_formats=[
            "Design expo",
            "Gallery walk",
            "Show-and-tell day"
        ]
    ),

    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Sketch storyboards",
            "Build simple models",
            "Create comic strips"
        ],
        kinesthetic_expression_options=[
            "Role-play user scenarios",
            "Use movement to show prototype function"
        ],
        verbal_expression_options=[
            "Explain your design journey",
            "Record a design podcast"
        ],
        collaborative_expression_options=[
            "Team presentations",
            "Peer interview panels"
        ],
        creative_expression_options=[
            "Write a short design journal",
            "Compose a design-themed song"
        ]
    ),

    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "User feedback is all negative",
            "Prototype breaks or fails",
            "Teams run out of ideas"
        ],
        student_interest_amplifiers=[
            "Offer new materials or constraints",
            "Connect to favorite games or toys"
        ],
        unexpected_connection_bridges=[
            "Link to art or storytelling",
            "Connect to science or math concepts"
        ],
        community_opportunity_integrators=[
            "Invite a local designer or maker",
            "Share at a school maker fair"
        ]
    ),

    getting_started_essentials=[
        "Gather diverse prototyping materials",
        "Prepare user research sheets",
        "Set up sketching and build areas"
    ],
    when_things_go_wrong=[
        "Prototypes fall apart: model simple fixes",
        "No testing volunteers: use stuffed animals or puppets",
        "Ideas stall: do a quick icebreakersketch"
    ],
    success_indicators=[
        "Students empathize with real users",
        "Many ideas are generated",
        "Prototypes function as intended",
        "Feedback is used to improve designs",
        "Reflections show learning"
    ],
    teacher_preparation_notes=[
        "Prepare a variety of prototyping supplies",
        "Model empathy interviews and sketching",
        "Arrange the room for team collaboration"
    ],
    common_challenges=[
        "Students focus on product over user needs",
        "Prototypes too detailed too soon",
        "Feedback sessions get distracted",
        "Iteration plans are skipped"
    ],
    teacher_prep_essentials=[
        "Print empathy and sketch templates",
        "Organize materials by station",
        "Plan a sample design demo"
    ],
    student_readiness="Great for grades 3–7 who enjoy hands-on making and sharing ideas.",
    community_engagement_level="Low – activities are class-based, with share-out for families or other classes.",
    assessment_highlights=[
        "Understanding of user needs",
        "Creativity of ideas",
        "Functionality of prototypes",
        "Use of feedback",
        "Depth of reflections"
    ],
    assessment_focus="Skills in empathy, ideation, prototyping, testing, and iteration.",
    what_success_looks_like="Students design and improve a working prototype that meets user needs and explain their process.",
    final_product_description="A final prototype accompanied by sketches, feedback notes, and a reflection journal.",

    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Empathy & Research",
            application="Students learn about user needs through interviews and observation.",
            assessment_connection="Assessed via clarity and relevance of research notes."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Creative Ideation",
            application="Students generate many ideas and select top options.",
            assessment_connection="Assessed via quantity and originality of ideas."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Prototyping & Iteration",
            application="Students build, test, and improve models.",
            assessment_connection="Assessed via prototype functionality and iteration changes."
        )
    ]
)
