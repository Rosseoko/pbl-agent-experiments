# templates/integration_skill/interdisciplinary.py

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

TEMPLATE = create_interdisciplinary_template = BaseTemplate(
    template_id="interdisciplinary",
    intent=TemplateIntent.INTERDISCIPLINARY,
    display_name="Interdisciplinary PBL Unit",
    description=(
        "Students tackle a real-world question by blending skills and ideas "
        "from two or more subjects, like science and art or math and social studies."
    ),
    pedagogical_approach="Integrative, inquiry-based learning across multiple disciplines",
    comprehensive_overview=(
        "In this unit, students pick a problem—such as designing a school garden that feeds pollinators, "
        "planning a mini-museum exhibit, or creating a recycling campaign. They use research, data, creativity, "
        "and communication skills from different subjects to plan, build, and share a solution. "
        "Along the way, they learn how subjects connect and why teamwork matters."
    ),
    driving_question_template="How can we use [Subject A] and [Subject B] to solve [authentic problem]?",

    core_learning_cycle=[
        "Project Launch & Plan",
        "Inquiry & Research",
        "Design & Create",
        "Share & Collaborate",
        "Reflect & Extend"
    ],

    essential_skills=[
        "critical_thinking",
        "research_and_inquiry",
        "creative_design",
        "data_analysis",
        "collaboration",
        "communication",
        "reflection"
    ],

    required_components=[
        "driving_question",
        "project_plan",
        "research_summary",
        "interdisciplinary_product",
        "presentation",
        "reflection_notes"
    ],

    natural_subject_areas=[
        SubjectArea.SCIENCE,
        SubjectArea.MATHEMATICS,
        SubjectArea.ENGLISH_LANGUAGE_ARTS,
        SubjectArea.SOCIAL_STUDIES
    ],

    cross_curricular_connections=[
        "Collecting and interpreting data",
        "Writing clear reports or scripts",
        "Visual design and art-making",
        "Team roles and project management",
        "Connecting content to community issues"
    ],

    entry_event_framework=EntryEventFramework(
        purpose="Spark interest with a mini challenge that blends two subjects",
        design_principles=[
            "Use concrete, relatable examples",
            "Encourage ‘I wonder…’ questions",
            "Show how subjects connect",
            "Keep it playful and hands-on"
        ],
        template_options=[
            EntryEventOption(
                type="mystery_box",
                example="Open a box containing natural objects and art supplies; ask: How could we show what these tell us?",
                student_response_pattern="Observe → brainstorm → share with partner",
                question_generation_method="What subjects help us tell this story?",
                estimated_time="20 minutes",
                materials_needed=["Box of items", "Paper", "Markers"]
            ),
            EntryEventOption(
                type="photo_gallery_walk",
                example="View photos of local places needing care; ask: How could we plan and share a solution?",
                student_response_pattern="Walk → note ideas → group share",
                question_generation_method="What will we need to know and do?",
                estimated_time="30 minutes",
                materials_needed=["Printed photos", "Sticky notes", "Chart paper"]
            )
        ],
        customization_guidance="Choose an entry event that highlights two subjects and student interests"
    ),

    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Project Launch & Plan",
            learning_purpose="Define the problem and plan how to research and solve it",
            core_activities=[
                "Brainstorm real-world problems",
                "Select one authentic challenge",
                "Write the driving question",
                "Outline project steps and roles"
            ],
            essential_deliverables=[
                "Chosen problem and question",
                "Project plan with tasks and subjects"
            ],
            reflection_checkpoints=[
                "Why does this matter?",
                "What subjects will help us?",
                "Who will do each task?"
            ],
            duration_scaling_notes="Sprint: Question only; Unit: Add plan; Journey: Detail roles"
        ),
        MilestoneTemplate(
            milestone_name="Inquiry & Research",
            learning_purpose="Gather information and data from multiple disciplines",
            core_activities=[
                "Conduct research using books, websites, or interviews",
                "Collect data (measurements, surveys)",
                "Take notes and organize findings"
            ],
            essential_deliverables=[
                "Research summary with facts and figures"
            ],
            reflection_checkpoints=[
                "What did we learn?",
                "Which facts support our idea?",
                "What questions remain?"
            ],
            duration_scaling_notes="Sprint: One source; Unit: 2–3 sources; Journey: 4+ sources"
        ),
        MilestoneTemplate(
            milestone_name="Design & Create",
            learning_purpose="Use research to design and build a solution",
            core_activities=[
                "Brainstorm design ideas",
                "Sketch or prototype the solution",
                "Gather materials and create final product"
            ],
            essential_deliverables=[
                "Sketches or models",
                "Finished prototype or plan"
            ],
            reflection_checkpoints=[
                "Does our design answer the question?",
                "How do subjects help shape it?"
            ],
            duration_scaling_notes="Sprint: Quick sketch; Unit: Basic prototype; Journey: Completed model"
        ),
        MilestoneTemplate(
            milestone_name="Share & Collaborate",
            learning_purpose="Present to peers and collect feedback",
            core_activities=[
                "Prepare a presentation or display",
                "Share with classmates or community",
                "Gather and record feedback"
            ],
            essential_deliverables=[
                "Presentation materials",
                "Feedback notes"
            ],
            reflection_checkpoints=[
                "What feedback was most helpful?",
                "How can we improve?"
            ],
            duration_scaling_notes="Same structure; vary audience size"
        ),
        MilestoneTemplate(
            milestone_name="Reflect & Extend",
            learning_purpose="Think about learning and plan next steps",
            core_activities=[
                "Write or draw a reflection on process",
                "Discuss how subjects connected",
                "Identify ways to extend or apply work"
            ],
            essential_deliverables=[
                "Reflection journal entry",
                "Next-step ideas"
            ],
            reflection_checkpoints=[
                "What did we learn about working together?",
                "How did subjects blend?",
                "What could we do differently?"
            ],
            duration_scaling_notes="Same depth for all durations"
        )
    ],

    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Plan Check",
                purpose="Ensure project plan is clear and balanced across subjects",
                implementation_guidance="Teacher reviews plan draft",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After planning",
                    Duration.JOURNEY: "Mid-research",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Quick look",
                    Duration.UNIT: "Basic feedback",
                    Duration.JOURNEY: "Detailed comments",
                    Duration.CAMPAIGN: "Rubric-based review"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Research Review",
                purpose="Check accuracy and relevance of research",
                implementation_guidance="Teacher or peer checks summary",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "Each source",
                    Duration.CAMPAIGN: "Weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Spot check",
                    Duration.UNIT: "Verbal feedback",
                    Duration.JOURNEY: "Written notes",
                    Duration.CAMPAIGN: "Peer and teacher combo"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Prototype Feedback",
                purpose="Gather early feedback on design drafts",
                implementation_guidance="Peers use a simple form",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After prototype",
                    Duration.JOURNEY: "Multiple rounds",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Quick notes",
                    Duration.UNIT: "Structured feedback",
                    Duration.JOURNEY: "Peer and teacher",
                    Duration.CAMPAIGN: "Community input"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Midpoint Showcase",
                purpose="Share research and plan progress",
                typical_timing="Mid-project",
                assessment_focus=["Research depth", "Plan clarity"],
                rubric_guidance="Evaluate evidence use and balance of subjects"
            ),
            SummativeAssessmentMoment(
                moment_name="Final Presentation",
                purpose="Present the interdisciplinary solution",
                typical_timing="Project end",
                assessment_focus=["Solution quality", "Presentation skills"],
                rubric_guidance="Assess how well subjects integrate and communicate"
            ),
            SummativeAssessmentMoment(
                moment_name="Peer Feedback Session",
                purpose="Give and receive constructive feedback",
                typical_timing="After presentation",
                assessment_focus=["Feedback quality", "Responsiveness"],
                rubric_guidance="Evaluate respect and usefulness of comments"
            ),
            SummativeAssessmentMoment(
                moment_name="Reflection Portfolio",
                purpose="Compile learning evidence and reflections",
                typical_timing="Project conclusion",
                assessment_focus=["Reflection depth", "Learning growth"],
                rubric_guidance="Assess insight and connections made"
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="Plus/Delta",
                purpose="Note positives and areas to improve",
                structure=[
                    "Plus: What went well?",
                    "Delta: What could we change?"
                ],
                timing_guidance="After presentations",
                facilitation_notes="Use chart paper for group share"
            ),
            ReflectionProtocol(
                protocol_name="3-2-1",
                purpose="Summarize learning with 3 successes, 2 questions, 1 new idea",
                structure=[
                    "3 things we did well",
                    "2 questions we still have",
                    "1 idea for next time"
                ],
                timing_guidance="Final reflection",
                facilitation_notes="Provide templates"
            )
        ],
        portfolio_guidance=(
            "Keep your plan, research notes, prototypes, feedback, and reflections together."
        )
    ),

    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teacher",
            "Other grade-level classes",
            "Family and community partners"
        ],
        engagement_formats=[
            "Class expo or gallery walk",
            "School showcase event",
            "Digital presentation or video"
        ],
        preparation_requirements=[
            "Practice your talk",
            "Check visuals and data",
            "Prepare to answer questions"
        ],
        logistical_considerations=[
            "Reserve display space",
            "Schedule event time",
            "Coordinate invites and tech"
        ]
    ),

    project_management_tools=[
        "Project timeline chart",
        "Research log",
        "Design storyboard",
        "Task checklist",
        "Feedback tracker"
    ],

    recommended_resources=[
        "Library books and articles",
        "Virtual field trips",
        "Art and craft supplies",
        "Data collection tools",
        "Online collaboration platforms"
    ],

    technology_suggestions=[
        "Tablets or computers",
        "Digital storytelling tools",
        "Data collection apps",
        "Presentation software",
        "Online meeting platforms"
    ],

    standards_alignment_examples={
        "science": [
            "NGSS 3-5-ETS1-1: Define a simple design problem reflecting a need or want.",
            "NGSS 4-PS3-2: Use evidence to explain phenomena."
        ],
        "mathematics": [
            "CCSS.MATH.CONTENT.4.MD.A.2: Represent and interpret data in graphs."
        ],
        "english_language_arts": [
            "CCSS.ELA-LITERACY.W.4.2: Write informative texts to examine a topic."
        ],
        "social_studies": [
            "C3.D2.Geo.3.3-5: Use maps to represent data."
        ],
        "cross_curricular": [
            "Collaboration and critical thinking across subjects"
        ]
    },

    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge=(
            "Students integrate concepts and skills from multiple disciplines "
            "to tackle a real problem."
        ),
        authenticity="Projects address genuine local or school-based needs.",
        public_product="A solution display or presentation that combines insights from different subjects.",
        collaboration="Teams plan and work together, sharing roles and responsibilities.",
        project_management="Structured timeline with checkpoints for research, design, and sharing.",
        reflection="Ongoing reflection on how subjects connect and learning growth."
    ),

    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN],
        social_structure_compatible=[SocialStructure.COLLABORATIVE, SocialStructure.NETWORKED],
        cognitive_complexity_range=[CognitiveComplexity.ANALYSIS, CognitiveComplexity.SYNTHESIS, CognitiveComplexity.EVALUATION],
        authenticity_compatible=[AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED],
        scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED],
        product_complexity_compatible=[ProductComplexity.PORTFOLIO, ProductComplexity.EXPERIENCE],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.HYBRID, DeliveryMode.SYNCHRONOUS_REMOTE]
    ),

    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we already know about our problem?",
            "What subjects can help us?"
        ],
        what_we_wonder_prompts=[
            "How might we combine ideas from different subjects?",
            "What questions guide our project?"
        ],
        what_we_want_to_learn_prompts=[
            "What research do we need in each subject?",
            "How will we measure success?"
        ],
        how_we_might_explore_options=[
            "Read books or watch videos",
            "Interview experts or peers",
            "Collect and analyze simple data"
        ],
        reflection_return_prompts=[
            "What surprised us about combining subjects?",
            "What will we try next?"
        ]
    ),

    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Research corner with books and tablets",
            "Sketching and prototyping tables",
            "Data display wall",
            "Reflection nook"
        ],
        documentation_displays=[
            "Project plans posted",
            "Research summaries on chart paper",
            "Prototype galleries",
            "Reflection boards"
        ],
        material_provocations=[
            "Mixed media supplies",
            "Data collection kits",
            "Subject prompt cards"
        ],
        collaboration_zones=[
            "Team workstations",
            "Peer feedback circles"
        ],
        reflection_retreats=[
            "Quiet journaling space",
            "Talking circle area"
        ]
    ),

    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Pick the problem to solve",
            "Choose research methods",
            "Decide prototype materials",
            "Select presentation format"
        ],
        voice_amplification_strategies=[
            "Students lead team discussions",
            "Peer teaching segments"
        ],
        ownership_transfer_milestones=[
            "Draft and revise project plan",
            "Manage research and creation steps"
        ],
        peer_collaboration_structures=[
            "Buddy checks",
            "Team critique sessions"
        ]
    ),

    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Photo-document research",
            "Record prototype steps",
            "Save sketches and notes",
            "Collect feedback forms",
            "Capture reflection entries"
        ],
        student_thinking_artifacts=[
            "Brainstorm charts",
            "Data tables",
            "Sketch drafts",
            "Prototype photos",
            "Reflection pages"
        ],
        process_documentation_methods=[
            "Project binder or digital folder",
            "Timeline posters"
        ],
        celebration_sharing_formats=[
            "Class gallery walk",
            "School showcase",
            "Digital slideshow"
        ]
    ),

    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Draw mind maps",
            "Create posters",
            "Build simple models"
        ],
        kinesthetic_expression_options=[
            "Act out processes",
            "Use role-play for presentations",
            "Manipulate physical data tokens"
        ],
        verbal_expression_options=[
            "Tell the story of your project",
            "Record a mini-podcast",
            "Explain findings to peers"
        ],
        collaborative_expression_options=[
            "Team presentations",
            "Peer interviews",
            "Group debates"
        ],
        creative_expression_options=[
            "Compose a song or poem",
            "Make a comic storyboard",
            "Design an infographic"
        ]
    ),

    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "New research changes direction",
            "Prototype fails initial test",
            "Teamwork challenges arise",
            "Data doesn’t fit plan",
            "Students pursue new interests"
        ],
        student_interest_amplifiers=[
            "Offer choice of additional materials",
            "Connect to students’ hobbies",
            "Invite voice from community helpers",
            "Allow extra research time",
            "Include creative play elements"
        ],
        unexpected_connection_bridges=[
            "Link to art or music",
            "Tie into local history",
            "Connect to math patterns",
            "Relate findings to everyday life",
            "Bridge to storytelling"
        ],
        community_opportunity_integrators=[
            "Invite a local expert",
            "Plan a field trip",
            "Share at family night",
            "Coordinate with another class",
            "Partner with a local organization"
        ]
    ),

    getting_started_essentials=[
        "Identify two subjects to integrate",
        "Gather basic research materials",
        "Set up team roles",
        "Prepare entry event supplies",
        "Arrange workspace zones"
    ],

    when_things_go_wrong=[
        "Research is off-topic: guide refocus",
        "Prototypes break: model quick fixes",
        "Team conflict: use discussion protocols",
        "Data is messy: show clear examples",
        "Time runs short: adjust scope"
    ],

    success_indicators=[
        "Clear, focused driving question",
        "Research uses multiple subjects",
        "Functional prototype or plan",
        "Engaging presentation",
        "Thoughtful reflections"
    ],

    teacher_preparation_notes=[
        "Gather diverse materials and sources",
        "Prepare guiding questions for each subject",
        "Set clear examples of integration",
        "Arrange room for teamwork",
        "Plan a demonstration"
    ],

    common_challenges=[
        "Balancing multiple subject demands",
        "Overloading project with too many ideas",
        "Keeping roles organized",
        "Communicating across disciplines",
        "Managing time effectively"
    ],

    teacher_prep_essentials=[
        "Print project plan templates",
        "Organize subject-specific resources",
        "Prepare reflection and feedback forms",
        "Plan sample project kickoff"
    ],

    student_readiness="Ideal for grades 3–7 who can collaborate and draw on multiple subjects with guidance.",

    community_engagement_level="Moderate – class-based with potential community showcase.",

    assessment_highlights=[
        "Depth and relevance of research",
        "Quality of interdisciplinary solution",
        "Effectiveness of presentation",
        "Insightfulness of reflections"
    ],

    assessment_focus="Skills in integrating knowledge, teamwork, creativity, and communication.",

    what_success_looks_like="Students combine subjects smoothly, create a working solution, and articulate their learning clearly.",

    final_product_description="A student-created project (model, plan, display or campaign) that uses at least two subjects, presented with evidence of research and reflection.",

    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Integration & Synthesis",
            application="Students combine ideas from different subjects into one solution.",
            assessment_connection="Assessed via how well subjects connect in their work."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Collaboration & Communication",
            application="Students plan, share, and reflect as a team.",
            assessment_connection="Assessed via quality of teamwork and presentations."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Creative Problem Solving",
            application="Students brainstorm, prototype, and refine solutions.",
            assessment_connection="Assessed via innovation and iteration in their projects."
        )
    ]
)
