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

TEMPLATE = create_technology_focused_template = BaseTemplate(
    template_id="technology_focused",
    intent=TemplateIntent.TECHNOLOGY_FOCUSED,
    display_name="Technology Focused Project (Grades 3–7)",
    description="Students in grades 3–7 explore simple technology and coding projects to solve fun challenges and share their creations.",
    pedagogical_approach="Tech-integrated PBL with hands-on building, block or simple text coding, and iterative design with peer feedback.",
    comprehensive_overview="""
In this Technology Focused Project, learners pick a fun challenge—like creating a simple game, animating a story, or building a basic robot. They learn coding steps or circuitry basics, plan and build prototypes, test with friends, and improve their designs. Finally, they share their projects in a class showcase. Through this, kids build computational thinking, creativity, and collaboration skills.
""",
    driving_question_template="How can we use [coding or simple electronics] to [solve a fun challenge] in a way that others can use or enjoy?",
    core_learning_cycle=[
        "Explore & Imagine",
        "Plan & Prototype",
        "Build & Test",
        "Refine & Retest",
        "Showcase & Reflect"
    ],
    essential_skills=[
        "computational_thinking",
        "basic_coding",
        "design_sketching",
        "problem_solving",
        "collaboration",
        "reflection"
    ],
    required_components=[
        "challenge_definition",
        "design_plan",
        "initial_prototype",
        "testing_feedback",
        "refined_prototype",
        "project_showcase",
        "process_reflection"
    ],
    natural_subject_areas=[
        SubjectArea.SCIENCE,
        SubjectArea.MATHEMATICS,
        SubjectArea.COMPUTER_SCIENCE
    ],
    cross_curricular_connections=[
        "Math: sequencing and logic",
        "Science: simple circuits and forces",
        "English: writing user instructions",
        "Art: visual design and storytelling",
        "Digital literacy: using tablets or microcontrollers"
    ],
    entry_event_framework=EntryEventFramework(
        purpose="Spark curiosity with cool tech demos and examples.",
        design_principles=[
            "Show playful tech examples",
            "Encourage wonder and questions",
            "Keep demos under 10 minutes",
            "Relate to familiar devices or games"
        ],
        template_options=[
            EntryEventOption(
                type="robot_demo",
                example="Show a simple robot moving or drawing",
                student_response_pattern="Watch → Ask questions → Draw ideas",
                question_generation_method="What would you make a robot do?",
                estimated_time="10 minutes",
                materials_needed=["Demo robot or video", "Paper", "Markers"]
            ),
            EntryEventOption(
                type="coding_game_start",
                example="Play a short block-coding game",
                student_response_pattern="Play → Discuss → Sketch next level",
                question_generation_method="How could you change this game?",
                estimated_time="10 minutes",
                materials_needed=["Tablet or computer with game"]
            )
        ],
        customization_guidance="Pick an entry that fits your available tech and keeps kids engaged."
    ),
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Explore & Imagine",
            learning_purpose="Understand the challenge and brainstorm ideas.",
            core_activities=[
                "Discuss the tech challenge",
                "Watch or try examples",
                "Brainstorm ideas and draw sketches"
            ],
            essential_deliverables=[
                "Challenge description",
                "Idea sketches"
            ],
            reflection_checkpoints=[
                "What excites you most?",
                "How will it work?"
            ],
            duration_scaling_notes="Short: one sketch; Longer: two sketches with pros/cons."
        ),
        MilestoneTemplate(
            milestone_name="Plan & Prototype",
            learning_purpose="Make a simple plan and build an initial prototype.",
            core_activities=[
                "Write or draw step-by-step plan",
                "Use blocks or simple circuits to build prototype"
            ],
            essential_deliverables=[
                "Plan sheet",
                "First prototype"
            ],
            reflection_checkpoints=[
                "Which part was easiest?",
                "Which part was tricky?"
            ],
            duration_scaling_notes="Short: one feature; Longer: two features."
        ),
        MilestoneTemplate(
            milestone_name="Build & Test",
            learning_purpose="Run and test the prototype with peers.",
            core_activities=[
                "Demonstrate prototype",
                "Gather peer feedback",
                "Note successes and issues"
            ],
            essential_deliverables=[
                "Test feedback notes",
                "Error log"
            ],
            reflection_checkpoints=[
                "What worked well?",
                "What needs fixing?"
            ],
            duration_scaling_notes="Single session or split across days."
        ),
        MilestoneTemplate(
            milestone_name="Refine & Retest",
            learning_purpose="Improve the prototype based on feedback.",
            core_activities=[
                "Make fixes or add features",
                "Retest with peers"
            ],
            essential_deliverables=[
                "Improved prototype",
                "New feedback notes"
            ],
            reflection_checkpoints=[
                "How is it better now?",
                "What else could improve?"
            ],
            duration_scaling_notes="Add one improvement per session."
        ),
        MilestoneTemplate(
            milestone_name="Showcase & Reflect",
            learning_purpose="Share final project and discuss learning.",
            core_activities=[
                "Present project in class",
                "Explain steps and challenges",
                "Reflect on what was learned"
            ],
            essential_deliverables=[
                "Final prototype",
                "Oral or written reflection"
            ],
            reflection_checkpoints=[
                "What did you learn?",
                "What would you try next time?"
            ],
            duration_scaling_notes="Include a 5-minute demo and talk."
        )
    ],
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Tech Journals",
                purpose="Record ideas, steps, and issues.",
                implementation_guidance="Draw or write one entry per session.",
                frequency_recommendations={
                    Duration.SPRINT: "Every day",
                    Duration.UNIT: "Each class",
                    Duration.JOURNEY: "Weekly",
                    Duration.CAMPAIGN: "Bi-weekly"
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
                moment_name="Prototype Demo",
                purpose="Show and explain the working prototype.",
                typical_timing="Mid-project",
                assessment_focus=["Functionality", "Creativity"],
                rubric_guidance="Use smiley faces or stars to rate success and ideas."
            ),
            SummativeAssessmentMoment(
                moment_name="Final Showcase",
                purpose="Demonstrate final tech project to class or family.",
                typical_timing="End of project",
                assessment_focus=["Effort", "Working solution"],
                rubric_guidance="3-star scale for effort and prototype success."
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="Peer Tech Talk",
                purpose="Discuss what worked and what to try next time.",
                structure=[
                    "What was coolest?",
                    "What was hardest?",
                    "What will you do differently?"
                ],
                timing_guidance="After final showcase",
                facilitation_notes="Use a circle time format for sharing."
            )
        ],
        portfolio_guidance="Save code screenshots, photos of prototypes, and journal pages."
    ),
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teacher",
            "Other classes in school",
            "Parents at home"
        ],
        engagement_formats=[
            "Class tech fair",
            "School showcase",
            "Simple demo video for families"
        ],
        preparation_requirements=[
            "Device charged",
            "Prototype on display",
            "Talking points or note cards"
        ],
        logistical_considerations=[
            "Power outlets",
            "USB or screen sharing setup",
            "Space for prototypes"
        ]
    ),
    project_management_tools=[
        "Project checklist",
        "Journal pages",
        "Prototype tracker",
        "Demo schedule"
    ],
    recommended_resources=[
        "Block-coding platforms (e.g., Scratch)",
        "Simple microcontroller kits (e.g., micro:bit)",
        "Online tutorials for kids",
        "Basic electronics kits"
    ],
    technology_suggestions=[
        "Tablets or computers with block coding",
        "Micro:bit or simple robotics sets",
        "Digital drawing tablets"
    ],
    standards_alignment_examples={
        "computer_science": [
            "CSTA K-2: Recognize that data can be represented by pictures and symbols."
        ],
        "mathematics": [
            "CCSS.MATH.CONTENT.3.OA.A.1: Interpret products of whole numbers."
        ],
        "science": [
            "3-5-ETS1-2: Develop a simple sketch, drawing, or physical model to illustrate how a device solves a problem."
        ]
    },
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge="Students solve real tech problems with simple coding or circuits.",
        authenticity="Functioning prototypes that classmates can use or view.",
        public_product="Tech fair or demo video shared with families.",
        collaboration="Pair or small-group building and testing.",
        project_management="Step-by-step planning with checklists.",
        reflection="Talking about successes and challenges."
    ),
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[
            Duration.SPRINT, Duration.UNIT
        ],
        social_structure_compatible=[
            SocialStructure.COLLABORATIVE, SocialStructure.INDIVIDUAL
        ],
        cognitive_complexity_range=[
            CognitiveComplexity.REMEMBERING, CognitiveComplexity.UNDERSTANDING, CognitiveComplexity.APPLICATION
        ],
        authenticity_compatible=[
            AuthenticityLevel.ANCHORED
        ],
        scaffolding_compatible=[
            ScaffoldingIntensity.HIGH, ScaffoldingIntensity.MEDIUM
        ],
        product_complexity_compatible=[
            ProductComplexity.ARTIFACT
        ],
        delivery_mode_compatible=[
            DeliveryMode.FACE_TO_FACE
        ]
    ),
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we know about coding or circuits?",
            "What devices have you used?"
        ],
        what_we_wonder_prompts=[
            "How does code make things happen?",
            "What could we build next?"
        ],
        what_we_want_to_learn_prompts=[
            "How do we fix errors in code?",
            "How does electricity flow?"
        ],
        how_we_might_explore_options=[
            "Try block code samples",
            "Experiment with simple circuits",
            "Research online child-friendly sites"
        ],
        reflection_return_prompts=[
            "What surprised you during building?",
            "What new ideas do you have now?"
        ]
    ),
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Coding station with tablets",
            "Maker corner with kits",
            "Quiet testing table"
        ],
        documentation_displays=[
            "Prototype photo board",
            "Code snippet displays",
            "Feedback sticky notes"
        ],
        material_provocations=[
            "Various sensors and wires",
            "Pre-built code blocks examples",
            "Circuit diagrams"
        ],
        collaboration_zones=[
            "Pair coding pods",
            "Group testing areas"
        ],
        reflection_retreats=[
            "Think nooks with headphones",
            "Sketch table for new ideas"
        ]
    ),
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Select challenge type (game, robot, animation)",
            "Choose tool or kit",
            "Decide how to present"
        ],
        voice_amplification_strategies=[
            "Student-led mini-tutorials",
            "Peer debugging sessions"
        ],
        ownership_transfer_milestones=[
            "Kids write their own code blocks",
            "Plan mini work sprints"
        ],
        peer_collaboration_structures=[
            "Buddy pair programming",
            "Group builder teams"
        ]
    ),
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Screen recordings of code runs",
            "Photos of circuit builds",
            "Journal sketches of ideas"
        ],
        student_thinking_artifacts=[
            "Flowchart diagrams",
            "Error logs"
        ],
        process_documentation_methods=[
            "Before-and-after demo videos",
            "Annotated code snippets"
        ],
        celebration_sharing_formats=[
            "Class tech festival",
            "Online showcase page"
        ]
    ),
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Animated stories",
            "Prototype posters"
        ],
        kinesthetic_expression_options=[
            "Robot dances",
            "Interactive installations"
        ],
        verbal_expression_options=[
            "Elevator code pitch",
            "Demo narration"
        ],
        collaborative_expression_options=[
            "Team coding challenges",
            "Demo relay races"
        ],
        creative_expression_options=[
            "Game jam session",
            "Light art with circuits"
        ]
    ),
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "When code errors are too many",
            "When circuit parts don’t fit"
        ],
        student_interest_amplifiers=[
            "Offer new sensors or blocks",
            "Invite tech-savvy peers to help"
        ],
        unexpected_connection_bridges=[
            "Link art and code",
            "Combine music and circuits"
        ],
        community_opportunity_integrators=[
            "Invite older students as mentors",
            "Share prototypes at school fair"
        ]
    ),
    teacher_preparation_notes=[
        "Install block-coding software",
        "Charge all devices and kits",
        "Arrange clear workspace",
        "Pre-load sample projects"
    ],
    common_challenges=[
        "Technical glitches and software bugs",
        "Power or connectivity issues",
        "Varied device familiarity",
        "Debugging frustration"
    ],
    getting_started_essentials=[
        "Ensure charged devices",
        "Set up block-coding accounts",
        "Prepare starter code examples"
    ],
    when_things_go_wrong=[
        "If code won’t run: restart device",
        "If parts missing: switch to drawing plan"
    ],
    signs_of_success=[
        "Prototype runs without errors",
        "Kids explain how it works",
        "They help peers debug"
    ],
    teacher_prep_essentials=[
        "Test kits and devices",
        "Prepare troubleshooting guide",
        "Arrange extension activities"
    ],
    student_readiness="Grades 3–7 comfortable with basic computers or tablets.",
    community_engagement_level="In-class or simple school tech showcase.",
    assessment_highlights=[
        "Working prototype",
        "Peer feedback and collaboration"
    ],
    assessment_focus="Functionality, creativity, and debugging skills.",
    what_success_looks_like="Students build and share a working tech project.",
    final_product_description="A simple game, animation, or device demo with explanation.",
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Computational Thinking",
            application="Breaking problems into steps and building solutions.",
            assessment_connection="Seen in code and prototype design."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Design & Prototyping",
            application="Sketching and building functional models.",
            assessment_connection="Seen in plan and prototype quality."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Collaboration & Debugging",
            application="Working together and fixing issues.",
            assessment_connection="Seen in peer testing notes and error fixes."
        )
    ]
)
