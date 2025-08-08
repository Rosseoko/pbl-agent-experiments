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

TEMPLATE = create_creative_expression_template = BaseTemplate(
    template_id="creative_expression",
    intent=TemplateIntent.CREATIVE_EXPRESSION,
    display_name="Creative Expression Fun Project (Grades 3–7)",
    description="Kids pick a theme—like ‘space’ or ‘animals’—and use art, music, drama, or digital tools to show their ideas.",
    pedagogical_approach="Hands‑on exploration, simple techniques, peer feedback, and show‑and‑tell presentations.",
    comprehensive_overview="""
Students in grades 3–7 choose a fun theme and bring it to life using drawing, painting, music, drama, or easy digital tools. They look at examples, try out techniques, share with friends, improve their work, and present it in a class showcase. Along the way, they practice creativity, sharing, and reflection.
""",
    driving_question_template="How can we use [drawing, music, drama, or digital tools] to share our theme in a fun way?",
    core_learning_cycle=[
        "Get Inspired",
        "Try & Sketch",
        "Create & Share",
        "Improve & Reflect",
        "Show & Tell"
    ],
    essential_skills=[
        "idea_generation",
        "basic_art_technique",
        "musical_expression",
        "performance_skills",
        "digital_creativity",
        "friendly_reflection"
    ],
    required_components=[
        "theme_choice",
        "inspiration_sketch",
        "first_version",
        "peer_feedback",
        "final_version",
        "showcase_event",
        "reflection_notes"
    ],
    natural_subject_areas=[
        SubjectArea.ARTS,
        SubjectArea.ENGLISH_LANGUAGE_ARTS,
        SubjectArea.SCIENCE  # e.g., themes like nature or space
    ],
    cross_curricular_connections=[
        "Reading stories about the theme",
        "Writing short captions",
        "Math: measuring or counting parts",
        "Science: exploring related topics",
        "Tech: using simple art or music apps"
    ],
    entry_event_framework=EntryEventFramework(
        purpose="Spark excitement with fun examples.",
        design_principles=[
            "Use bright, relatable examples",
            "Keep activities under 15 minutes",
            "Ask open questions: ‘What do you notice?’",
            "Encourage quick hands‑on trials"
        ],
        template_options=[
            EntryEventOption(
                type="gallery_walk",
                example="Show pictures or videos about different creative works",
                student_response_pattern="Look → Talk → Quick sketch",
                question_generation_method="What do you like? What would you try?",
                estimated_time="15 minutes",
                materials_needed=["Images or videos", "Paper", "Crayons"]
            ),
            EntryEventOption(
                type="guest_demo",
                example="Invite a student or teacher to demonstrate a creative skill",
                student_response_pattern="Watch → Ask questions → Try it",
                question_generation_method="Which part looks fun? Which part is tricky?",
                estimated_time="15 minutes",
                materials_needed=["Demo materials"]
            )
        ],
        customization_guidance="Choose an entry that fits your class interests and time."
    ),
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Get Inspired",
            learning_purpose="Gather ideas and pick a theme.",
            core_activities=[
                "Discuss examples",
                "Share favorite ideas",
                "Choose a theme",
                "Draw a quick sketch"
            ],
            essential_deliverables=[
                "Theme name",
                "One‑page sketch"
            ],
            reflection_checkpoints=[
                "Why did I choose this theme?",
                "What story will I tell?"
            ],
            duration_scaling_notes="Short: sketch only; Longer: sketch + caption."
        ),
        MilestoneTemplate(
            milestone_name="Try & Sketch",
            learning_purpose="Experiment with materials and plan your piece.",
            core_activities=[
                "Try different tools",
                "Make small drafts",
                "Plan your final work"
            ],
            essential_deliverables=[
                "Draft sketches or drafts",
                "Materials list"
            ],
            reflection_checkpoints=[
                "Which draft did I like best?",
                "What will I keep?"
            ],
            duration_scaling_notes="Sprint: one draft; Unit: two drafts; Journey: three+ drafts."
        ),
        MilestoneTemplate(
            milestone_name="Create & Share",
            learning_purpose="Make and show your first version.",
            core_activities=[
                "Create the first version",
                "Share with a partner",
                "Collect simple feedback"
            ],
            essential_deliverables=[
                "First version",
                "Peer feedback notes"
            ],
            reflection_checkpoints=[
                "What did my partner like?",
                "What can I change?"
            ],
            duration_scaling_notes="One session or split across days."
        ),
        MilestoneTemplate(
            milestone_name="Improve & Reflect",
            learning_purpose="Use feedback to make it better.",
            core_activities=[
                "Apply feedback",
                "Add details",
                "Reflect on changes"
            ],
            essential_deliverables=[
                "Updated version",
                "Reflection journal"
            ],
            reflection_checkpoints=[
                "How is it different now?",
                "What did I learn?"
            ],
            duration_scaling_notes="Improve one part at a time."
        ),
        MilestoneTemplate(
            milestone_name="Show & Tell",
            learning_purpose="Present your final work and talk about it.",
            core_activities=[
                "Set up a mini exhibit",
                "Explain your process",
                "Listen to audience responses"
            ],
            essential_deliverables=[
                "Final piece",
                "One‑sentence reflection"
            ],
            reflection_checkpoints=[
                "What did I enjoy most?",
                "What would I try next?"
            ],
            duration_scaling_notes="5–10 minute class showcase."
        )
    ],
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Sketch Journal",
                purpose="Draw or write quick notes each session.",
                implementation_guidance="Keep it simple: picture + caption.",
                frequency_recommendations={
                    Duration.SPRINT: "Every day",
                    Duration.UNIT: "Each session",
                    Duration.JOURNEY: "Weekly",
                    Duration.CAMPAIGN: "Bi‑weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "One entry",
                    Duration.UNIT: "Two entries",
                    Duration.JOURNEY: "Three entries",
                    Duration.CAMPAIGN: "Four entries"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Mid‑Project Share",
                purpose="Show drafts and gather simple feedback.",
                typical_timing="Midway",
                assessment_focus=["Creativity", "Effort"],
                rubric_guidance="Use stickers or smileys for feedback."
            ),
            SummativeAssessmentMoment(
                moment_name="Final Showcase",
                purpose="Present finished work to class or families.",
                typical_timing="End of project",
                assessment_focus=["Effort", "Expression"],
                rubric_guidance="1–3 stars for expression and effort."
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="Circle Chat",
                purpose="Talk about favorites and next steps.",
                structure=[
                    "What did I like best?",
                    "What surprised me?",
                    "What will I do differently next time?"
                ],
                timing_guidance="After showcase",
                facilitation_notes="Sit in a circle and share."
            )
        ],
        portfolio_guidance="Keep sketches, feedback notes, and a photo of final work."
    ),
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=["Classmates","Families","School display"],
        engagement_formats=["Classroom gallery","Hallway board","Video slideshow"],
        preparation_requirements=["Paper or tablet","Labels or captions","Invitation notes"],
        logistical_considerations=["Wall space","Time slot","Help from teacher"]
    ),
    project_management_tools=["Idea chart","Sketch journal","Feedback stickers","Showcase plan"],
    recommended_resources=["Crayons and paper","Music instruments","Simple drama props","Kid-friendly apps"],
    technology_suggestions=["Drawing apps","Audio recorder apps","Photo cameras"],
    standards_alignment_examples={
        "arts": ["VA:Cr1.1.3: Explore ideas through art and design."],
        "english_language_arts": ["CCSS.ELA-LITERACY.W.3.3: Write narratives with details."]
    },
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge="Kids make original creations that share ideas.",
        authenticity="Real classmates and families see their work.",
        public_product="Class showcase or display.",
        collaboration="Partner feedback and group planning.",
        project_management="Simple steps with checklists.",
        reflection="Talking about what worked and what to try next."
    ),
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT,Duration.UNIT],
        social_structure_compatible=[SocialStructure.INDIVIDUAL,SocialStructure.COLLABORATIVE],
        cognitive_complexity_range=[CognitiveComplexity.REMEMBERING,CognitiveComplexity.UNDERSTANDING,CognitiveComplexity.APPLICATION],
        authenticity_compatible=[AuthenticityLevel.ANCHORED],
        scaffolding_compatible=[ScaffoldingIntensity.HIGH,ScaffoldingIntensity.MEDIUM],
        product_complexity_compatible=[ProductComplexity.ARTIFACT],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE]
    ),
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=["What do we know about our theme?","What have we seen?"],
        what_we_wonder_prompts=["What else do we want to learn?","What questions are we curious about?"],
        what_we_want_to_learn_prompts=["How can we show our theme best?","What tools will help?"],
        how_we_might_explore_options=["Try drawing","Make music","Act it out","Use a simple app"],
        reflection_return_prompts=["What surprised us?","What new ideas do we have?"]
    ),
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=["Art corner with supplies","Music station","Drama area"],
        documentation_displays=["Work-in-progress wall","Feedback sticky notes","Photo collage"],
        material_provocations=["Various markers and paints","Simple instruments","Props and costumes"],
        collaboration_zones=["Buddy tables","Group circle"],
        reflection_retreats=["Quiet nook","Listening corner"]
    ),
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=["Pick theme","Choose medium","Decide who to share with"],
        voice_amplification_strategies=["Student-led demos","Peer compliments"],
        ownership_transfer_milestones=["Kids plan their steps","Choose feedback to use"],
        peer_collaboration_structures=["Buddy feedback sessions","Group planning" ]
    ),
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=["Sketchbook pages","Audio clips","Photo diary"],
        student_thinking_artifacts=["Idea webs","Draft notes"],
        process_documentation_methods=["Before/after photos","Annotated drafts"],
        celebration_sharing_formats=["Gallery walk","Video montage"]
    ),
    expression_pathways=ExpressionPathways(
        visual_expression_options=["Posters","Photo stories"],
        kinesthetic_expression_options=["Simple drama","Group mural"],
        verbal_expression_options=["Mini presentations","Storytelling"],
        collaborative_expression_options=["Team mural","Group song"],
        creative_expression_options=["Stop-motion video","Music composition"]
    ),
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=["When new ideas pop up","When a tool doesn’t work"],
        student_interest_amplifiers=["Offer new materials","Let kids lead demos"],
        unexpected_connection_bridges=["Link art and music","Blend drama and drawing"],
        community_opportunity_integrators=["Invite younger buddies","Share at school assembly"]
    ),
    teacher_preparation_notes=["Gather safe art supplies","Set up simple apps","Plan quick demos","Arrange display space"],
    common_challenges=["Short attention spans","Messy materials","Different skill levels","Need clear instructions","Sharing politely"],
    getting_started_essentials=["Theme list","Sketch paper","Art supplies"],
    when_things_go_wrong=["If kids get stuck: show example","If supplies run out: switch to drawing"],
    signs_of_success=["Kids smile sharing","They talk about their work","They try new ideas"],
    teacher_prep_essentials=["Prepare theme cards","Test supplies","Plan showtime"],
    student_readiness="Grades 3–7 comfortable with drawing, music, or drama basics.",
    community_engagement_level="Classroom or small display area.",
    assessment_highlights=["Creativity","Effort","Sharing"],
    assessment_focus="Creative process, expression, and collaboration.",
    what_success_looks_like="Kids create and share work that shows their ideas.",
    final_product_description="An art piece, performance, or digital creation with a short talk.",
    core_skills=[
        BaseTemplate.CoreSkill("Creative Thinking","Trying new ideas.","Seen in unique work."),
        BaseTemplate.CoreSkill("Basic Technique","Using tools well.","Seen in final piece."),
        BaseTemplate.CoreSkill("Sharing & Listening","Presenting and giving feedback.","Seen in show-and-tell.")
    ]
)
