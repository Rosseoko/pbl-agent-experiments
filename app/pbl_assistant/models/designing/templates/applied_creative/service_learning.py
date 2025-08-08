from pydantic import Field
from typing import List, Dict
from app.pbl_assistant.models.designing.core.base_template import (
    BaseTemplate,
    EntryEventFramework,
    EntryEventOption,
    MilestoneTemplate,
    AssessmentFramework,
    FormativeAssessmentTool,
    SummativeAssessmentMoment,
    ReflectionProtocol,
    AuthenticAudienceFramework,
    HQPBLAlignment,
    CompatibilityMatrix,
    InquiryFramework,
    LearningEnvironmentFramework,
    StudentAgencyFramework,
    DocumentationFramework,
    ExpressionPathways,
    EmergentLearningSupport
)
from app.pbl_assistant.models.designing.core.enums import (
    TemplateIntent,
    Duration,
    SocialStructure,
    CognitiveComplexity,
    AuthenticityLevel,
    ScaffoldingIntensity,
    ProductComplexity,
    DeliveryMode,
    SubjectArea
)

TEMPLATE = create_service_learning_template = BaseTemplate(
    template_id="service_learning",
    intent=TemplateIntent.SERVICE_LEARNING,
    display_name="Service Learning Project (Grades 3–7)",
    description="Students learn about community needs and work together on simple service projects that help others.",
    pedagogical_approach="Community-centered PBL with hands-on activities, collaboration, and reflection for young learners.",
    comprehensive_overview="""
In this Service Learning project, students in grades 3–7 explore a local need (like helping a park, library, or animal shelter), plan a small project, work together to make a difference, and share what they learned. They practice kindness, teamwork, and problem-solving through age-appropriate activities and a fun, supportive process.
""",
    driving_question_template="How can we [help our community/home/school] by doing a simple service project?",
    core_learning_cycle=[
        "Discover & Care",
        "Plan & Prepare",
        "Serve & Help",
        "Share & Reflect"
    ],
    essential_skills=[
        "empathy",
        "teamwork",
        "planning",
        "simple_research",
        "communication",
        "reflection"
    ],
    required_components=[
        "community_need",
        "project_plan",
        "materials_list",
        "action_steps",
        "service_activity",
        "group_reflection",
        "share_out"
    ],
    natural_subject_areas=[
        SubjectArea.SOCIAL_STUDIES,
        SubjectArea.SCIENCE,
        SubjectArea.ENGLISH_LANGUAGE_ARTS
    ],
    cross_curricular_connections=[
        "Reading about community helpers",
        "Writing simple plans or thank-you notes",
        "Basic math for counting supplies",
        "Science: caring for plants or animals",
        "Art: creating posters or cards"
    ],
    entry_event_framework=EntryEventFramework(
        purpose="Introduce students to community helpers and local needs.",
        design_principles=[
            "Use pictures and stories",
            "Encourage questions and ideas",
            "Keep it short and engaging",
            "Connect to things they know"
        ],
        template_options=[
            EntryEventOption(
                type="community_helper_story",
                example="Read a picture book about firefighters or park rangers",
                student_response_pattern="Listen → Discuss → Draw favorite part",
                question_generation_method="What do helpers do? How can we help?",
                estimated_time="15 minutes",
                materials_needed=["Book", "Paper", "Crayons"]
            ),
            EntryEventOption(
                type="neighborhood_walk",
                example="Short walk to observe litter or plants needing care",
                student_response_pattern="Walk → Note what you see → Share"
,                question_generation_method="What could make this place nicer?",
                estimated_time="20 minutes",
                materials_needed=["Clipboards", "Pencils"]
            )
        ],
        customization_guidance="Choose an entry that fits your school or neighborhood setting."
    ),
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Discover & Care",
            learning_purpose="Identify a simple community need and show care.",
            core_activities=[
                "Talk about helpers and needs",
                "Observe our school or neighborhood",
                "Pick one need to focus on"
            ],
            essential_deliverables=[
                "Chosen need (e.g., clean-up, plant care)",
                "Why it matters (sentence)"
            ],
            reflection_checkpoints=[
                "Why did we pick this?",
                "Who will it help?"
            ],
            duration_scaling_notes="Quick: one need; Longer: compare two needs."
        ),
        MilestoneTemplate(
            milestone_name="Plan & Prepare",
            learning_purpose="Create a simple plan and gather materials.",
            core_activities=[
                "List steps to help",
                "Count and gather supplies",
                "Assign roles in the group"
            ],
            essential_deliverables=[
                "Step-by-step plan",
                "Materials list",
                "Team roles"
            ],
            reflection_checkpoints=[
                "Who will do each task?",
                "Do we have what we need?"
            ],
            duration_scaling_notes="Short: 2–3 steps; Longer: detail timing."
        ),
        MilestoneTemplate(
            milestone_name="Serve & Help",
            learning_purpose="Carry out the service activity as a team.",
            core_activities=[
                "Follow our plan",
                "Work together",
                "Help each other"
            ],
            essential_deliverables=[
                "Photos or notes of action",
                "Count of items cleaned or planted"
            ],
            reflection_checkpoints=[
                "What went well?",
                "What was hard?"
            ],
            duration_scaling_notes="Single session or multiple days."
        ),
        MilestoneTemplate(
            milestone_name="Share & Reflect",
            learning_purpose="Share what we did and how we felt.",
            core_activities=[
                "Create thank-you cards or posters",
                "Present to class or families",
                "Talk about our feelings"
            ],
            essential_deliverables=[
                "Thank-you cards/posters",
                "Short presentation",
                "Group reflection"
            ],
            reflection_checkpoints=[
                "How did helping feel?",
                "What did we learn about teamwork?"
            ],
            duration_scaling_notes="Include a 5-minute share-out."
        )
    ],
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Service Journals",
                purpose="Record daily thoughts and steps.",
                implementation_guidance="Draw or write one thing each day.",
                frequency_recommendations={
                    Duration.SPRINT: "Every day",
                    Duration.UNIT: "Each session",
                    Duration.JOURNEY: "Weekly",
                    Duration.CAMPAIGN: "Every two weeks"
                },
                scaling_guidance={
                    Duration.SPRINT: "One note",
                    Duration.UNIT: "Two notes",
                    Duration.JOURNEY: "Three notes",
                    Duration.CAMPAIGN: "Four notes"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Project Mid-Share",
                purpose="Show progress and get classmates’ ideas.",
                typical_timing="Mid-project",
                assessment_focus=["Effort", "Teamwork"],
                rubric_guidance="Thumbs-up or helpful suggestion."
            ),
            SummativeAssessmentMoment(
                moment_name="Final Share-Out",
                purpose="Present what we did and how it helped.",
                typical_timing="End of project",
                assessment_focus=["Participation", "Reflection"],
                rubric_guidance="Star stickers for great teamwork and care."
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="Circle Talk",
                purpose="Discuss feelings and learnings together.",
                structure=[
                    "What felt good?",
                    "What surprised you?",
                    "What will we do next time?"
                ],
                timing_guidance="After final share-out",
                facilitation_notes="Sit in a circle and take turns talking."
            )
        ],
        portfolio_guidance="Keep photos, drawings, and notes in a simple folder."
    ),
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teachers",
            "Families",
            "School community boards"
        ],
        engagement_formats=[
            "Class presentation",
            "Hallway display",
            "Short video for parents"
        ],
        preparation_requirements=[
            "Photos or drawings",
            "Posters or cards",
            "Invitation notes"
        ],
        logistical_considerations=[
            "Display space",
            "Time to set up",
            "Audio volume if needed"
        ]
    ),
    project_management_tools=[
        "Simple checklist",
        "Service journal pages",
        "Thank-you card templates",
        "Share-out planner"
    ],
    recommended_resources=[
        "Local park or library contacts",
        "Recyclable materials",
        "Art supplies for cards",
        "Kid-friendly gloves and tools"
    ],
    technology_suggestions=[
        "Tablet for photos",
        "Simple drawing app",
        "Camera with easy buttons"
    ],
    standards_alignment_examples={
        "social_studies": [
            "SS:3.CG.1.1: Explain the roles of community members.",
            "SS:4.CG.2.1: Describe how individuals contribute to communities."
        ],
        "science": [
            "3-LS4-3: Construct an argument with evidence that in a particular habitat, some organisms can survive well…"
        ],
        "english_language_arts": [
            "CCSS.ELA-LITERACY.W.3.2: Write informative/explanatory texts to examine a topic."
        ]
    },
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge="Students identify and address real needs with simple plans.",
        authenticity="Real service to real community or school spaces.",
        public_product="Helped space (clean, decorated) and shared work.",
        collaboration="Working in small teams with clear roles.",
        project_management="Step-by-step plan with checklists.",
        reflection="Talking about feelings and lessons learned."
    ),
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[
            Duration.SPRINT, Duration.UNIT
        ],
        social_structure_compatible=[
            SocialStructure.COLLABORATIVE
        ],
        cognitive_complexity_range=[
            CognitiveComplexity.REMEMBERING, CognitiveComplexity.UNDERSTANDING, CognitiveComplexity.APPLICATION
        ],
        authenticity_compatible=[
            AuthenticityLevel.ANCHORED
        ],
        scaffolding_compatible=[
            ScaffoldingIntensity.HIGH
        ],
        product_complexity_compatible=[
            ProductComplexity.EXPERIENCE
        ],
        delivery_mode_compatible=[
            DeliveryMode.FACE_TO_FACE
        ]
    ),
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we already know about helpers in our community?",
            "What places or people need help?"
        ],
        what_we_wonder_prompts=[
            "How can we help?",
            "What resources do we need?"
        ],
        what_we_want_to_learn_prompts=[
            "What steps will make our service work?",
            "Who can we ask for advice?"
        ],
        how_we_might_explore_options=[
            "Research helpers online or in books",
            "Talk to a teacher or parent",
            "Draw our own plan"
        ],
        reflection_return_prompts=[
            "What did we learn about helping?",
            "What would we do differently next time?"
        ]
    ),
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Service station with supplies",
            "Display area for work-in-progress",
            "Group workspace tables"
        ],
        documentation_displays=[
            "Photo wall of service activity",
            "Reflection quote board",
            "Materials checklist display"
        ],
        material_provocations=[
            "Gloves, trash bags, art supplies",
            "Reference books or posters"
        ],
        collaboration_zones=[
            "Buddy pairs",
            "Small groups"
        ],
        reflection_retreats=[
            "Quiet corners for drawing feelings",
            "Circle seats for talk time"
        ]
    ),
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Pick a need to address",
            "Choose which task to do",
            "Decide how to share results"
        ],
        voice_amplification_strategies=[
            "Student-led demonstration",
            "Helping younger classmates"
        ],
        ownership_transfer_milestones=[
            "Kids lead parts of the service",
            "Plan next steps after feedback"
        ],
        peer_collaboration_structures=[
            "Group roles (leader, helper, recorder)",
            "Peer-helper buddies"
        ]
    ),
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Photos of service in action",
            "Drawing journals",
            "Simple charts of items collected"
        ],
        student_thinking_artifacts=[
            "Idea maps",
            "Reflection stickers"
        ],
        process_documentation_methods=[
            "Before-and-after photos",
            "Checklist completion charts"
        ],
        celebration_sharing_formats=[
            "Class awards ceremony",
            "Thank-you assembly"
        ]
    ),
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Posters or murals",
            "Photo collages"
        ],
        kinesthetic_expression_options=[
            "Group clean-up dance",
            "Role-play safety rules"
        ],
        verbal_expression_options=[
            "Short speeches",
            "Thank-you songs"
        ],
        collaborative_expression_options=[
            "Team chant",
            "Group presentation"
        ],
        creative_expression_options=[
            "Simple skits",
            "DIY thank-you cards"
        ]
    ),
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "When kids find new needs",
            "When tools aren’t working"
        ],
        student_interest_amplifiers=[
            "Offer extra roles",
            "Let kids share ideas aloud"
        ],
        unexpected_connection_bridges=[
            "Link art with service",
            "Use math to count recycled items"
        ],
        community_opportunity_integrators=[
            "Invite parent volunteers",
            "Share work at school assembly"
        ]
    ),
    teacher_preparation_notes=[
        "Prepare safe supplies (gloves, bags)",
        "Plan short example demo",
        "Set up clear work areas",
        "Notify helpers or partners"
    ],
    common_challenges=[
        "Keeping kids focused",
        "Managing supplies",
        "Different pace of work",
        "Ensuring safety"
    ],
    getting_started_essentials=[
        "Simple idea list",
        "Basic supplies",
        "Group assignment plan"
    ],
    when_things_go_wrong=[
        "If kids are tired: take a short break",
        "If supplies run out: switch to drawing"
    ],
    signs_of_success=[
        "Kids talk about helping",
        "They smile and work together",
        "They show their work proudly"
    ],
    teacher_prep_essentials=[
        "Gather helpers or volunteers",
        "Test supplies",
        "Plan share time"
    ],
    student_readiness="Grades 3–7 comfortable with simple tasks and teamwork.",
    community_engagement_level="In-class or small school area projects.",
    assessment_highlights=[
        "Teamwork and care shown",
        "Completion of service steps"
    ],
    assessment_focus="Participation, empathy, and effort.",
    what_success_looks_like="Kids help someone or something and talk about how it felt.",
    final_product_description="A cleaner space, planted area, or cards made with photos or drawings.",
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Empathy & Care",
            application="Seeing and acting on others’ needs.",
            assessment_connection="Seen in conversations and actions."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Planning & Teamwork",
            application="Organizing simple steps and working together.",
            assessment_connection="Seen in completed plans and cooperation."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Reflection & Sharing",
            application="Talking about what was done and learned.",
            assessment_connection="Seen in share-out and journals."
        )
    ]
)
