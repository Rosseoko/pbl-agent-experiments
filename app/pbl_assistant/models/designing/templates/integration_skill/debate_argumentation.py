# templates/integration_skill/debate_argumentation.py

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

TEMPLATE = create_debate_argumentation_template = BaseTemplate(
    template_id="debate_argumentation",
    intent=TemplateIntent.DEBATE_ARGUMENTATION,
    display_name="Debate & Argumentation Project",
    description=(
        "Students learn to think and speak like polite debaters: they explore both sides "
        "of a question, gather reasons with examples, share their ideas respectfully, "
        "and listen to others."
    ),
    pedagogical_approach="Argumentation and critical thinking through structured debate",
    comprehensive_overview=(
        "In this project, students pick a simple, kid-friendly question—like "
        "'Should class have longer recess?' or 'Which pet is best, cats or dogs?'—"
        "They research reasons for both sides, practice opening statements and rebuttals, "
        "hold a mini-debate, then reflect on what they learned about listening, evidence, "
        "and respect for different opinions."
    ),
    driving_question_template="Which side of [issue] has the strongest reasons, and why?",
    
    core_learning_cycle=[
        "Ask & Choose Topic",
        "Research Reasons",
        "Plan & Practice",
        "Debate & Listen",
        "Reflect & Connect"
    ],
    
    essential_skills=[
        "question_formulation",
        "reasoning_with_evidence",
        "speech_planning",
        "public_speaking",
        "active_listening",
        "respectful_discussion",
        "reflection"
    ],
    
    required_components=[
        "driving_question",
        "pro_con_reasons",
        "opening_statement",
        "rebuttal_points",
        "closing_statement",
        "reflection_notes"
    ],
    
    natural_subject_areas=[
        SubjectArea.ENGLISH_LANGUAGE_ARTS,
        SubjectArea.SOCIAL_STUDIES
    ],
    
    cross_curricular_connections=[
        "Writing opinion pieces",
        "Reading informational texts",
        "Social studies themes",
        "Listening and speaking skills",
        "Graphic organizers (T-charts)"
    ],
    
    entry_event_framework=EntryEventFramework(
        purpose="Spark interest with a fun agree/disagree poll or sample debate clip",
        design_principles=[
            "Use simple, relatable statements",
            "Model respectful disagreement",
            "Encourage ‘I wonder…’ questions",
            "Keep it brief and engaging"
        ],
        template_options=[
            EntryEventOption(
                type="agree_disagree_poll",
                example="Read 'I like superhero movies more than cartoons.' Thumbs-up/down, then ask why.",
                student_response_pattern="Vote → share one reason → discuss with partner",
                question_generation_method="What makes you agree or disagree?",
                estimated_time="15 minutes",
                materials_needed=["Statement cards", "Thumbs-up/down signal"]
            ),
            EntryEventOption(
                type="mini_debate_demo",
                example="Show a short video of kids debating 'Should pizza be served every day?'",
                student_response_pattern="Watch → list reasons heard → share with class",
                question_generation_method="What reasons did each side give?",
                estimated_time="10 minutes",
                materials_needed=["Video clip or script", "Paper and pencil"]
            )
        ],
        customization_guidance="Pick the entry event that best fits your class time and resources"
    ),
    
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Ask & Choose Topic",
            learning_purpose="Generate fun questions and pick one to debate",
            core_activities=[
                "Brainstorm classroom questions",
                "Use question starters (Should…? Which is better…?)",
                "Vote on favorites",
                "Choose one question as the debate topic"
            ],
            essential_deliverables=[
                "List of 3–5 questions",
                "Selected debate question"
            ],
            reflection_checkpoints=[
                "Which question seems most interesting?",
                "Why did our class choose this topic?"
            ],
            duration_scaling_notes="Sprint: List only; Unit: Choose topic; Journey: Add voting results"
        ),
        MilestoneTemplate(
            milestone_name="Research Reasons",
            learning_purpose="Find at least two reasons for each side of the question",
            core_activities=[
                "Work in teams to list reasons pro and con",
                "Use books, websites, or talk to classmates",
                "Write examples or draw pictures"
            ],
            essential_deliverables=[
                "Pro/con reasons chart with 2+ reasons each"
            ],
            reflection_checkpoints=[
                "Which side was easier to find reasons for?",
                "What examples help our reasons?"
            ],
            duration_scaling_notes="Sprint: 1 reason each; Unit: 2 reasons each; Journey: 3+ reasons each"
        ),
        MilestoneTemplate(
            milestone_name="Plan & Practice",
            learning_purpose="Write and practice opening statements and rebuttals",
            core_activities=[
                "Draft opening statements with reasons",
                "Plan one rebuttal for the opposite side",
                "Practice speaking in pairs"
            ],
            essential_deliverables=[
                "Scripted opening and rebuttal notes"
            ],
            reflection_checkpoints=[
                "Is our statement clear?",
                "Do we have evidence to share?"
            ],
            duration_scaling_notes="Sprint: Opening only; Unit: Opening + one rebuttal; Journey: Add closing statement"
        ),
        MilestoneTemplate(
            milestone_name="Debate & Listen",
            learning_purpose="Conduct the debate, speak clearly, and listen respectfully",
            core_activities=[
                "Hold timed opening statements",
                "Share rebuttals",
                "Listen without interrupting",
                "Take notes on what others say"
            ],
            essential_deliverables=[
                "Debate session notes",
                "Peer feedback comments"
            ],
            reflection_checkpoints=[
                "How well did we listen?",
                "Which new reasons did we hear?"
            ],
            duration_scaling_notes="Same activities; vary time per round by duration"
        ),
        MilestoneTemplate(
            milestone_name="Reflect & Connect",
            learning_purpose="Think about what we learned and how to use debate skills",
            core_activities=[
                "Write or draw reflections on the process",
                "Discuss how debate skills help in real life",
                "Share one thing you’d do differently next time"
            ],
            essential_deliverables=[
                "Reflection journal entry",
                "Class discussion summary"
            ],
            reflection_checkpoints=[
                "What was our biggest learning?",
                "How did our opinion change?"
            ],
            duration_scaling_notes="Same depth for all durations"
        )
    ],
    
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Reason Chart Check",
                purpose="Ensure students list clear reasons with examples",
                implementation_guidance="Teacher reviews pro/con charts mid-project",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "After research",
                    Duration.CAMPAIGN: "Weekly check"
                },
                scaling_guidance={
                    Duration.SPRINT: "Spot check",
                    Duration.UNIT: "Basic feedback",
                    Duration.JOURNEY: "Detailed notes",
                    Duration.CAMPAIGN: "Peer review added"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Speaking Practice Log",
                purpose="Monitor clarity and volume during practice",
                implementation_guidance="Peers give feedback during rehearsals",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After practice",
                    Duration.JOURNEY: "Each session",
                    Duration.CAMPAIGN: "Weekly logs"
                },
                scaling_guidance={
                    Duration.SPRINT: "Quick thumbs up/down",
                    Duration.UNIT: "Verbal praise and tips",
                    Duration.JOURNEY: "Written feedback",
                    Duration.CAMPAIGN: "Rubric-based"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Peer Feedback Check",
                purpose="Ensure respectful listening and notes",
                implementation_guidance="Peers fill out simple feedback forms",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "Each debate round",
                    Duration.CAMPAIGN: "After each session"
                },
                scaling_guidance={
                    Duration.SPRINT: "Emoji reactions",
                    Duration.UNIT: "Short comments",
                    Duration.JOURNEY: "Structured form",
                    Duration.CAMPAIGN: "Rubric + comments"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Opening Statements",
                purpose="Present clear reasons at the start",
                typical_timing="During debate phase",
                assessment_focus=["Clarity", "Evidence"],
                rubric_guidance="Assess strength and clarity of reasons"
            ),
            SummativeAssessmentMoment(
                moment_name="Rebuttal Performance",
                purpose="Respond to the opposite side respectfully",
                typical_timing="During debate phase",
                assessment_focus=["Listening", "Response quality"],
                rubric_guidance="Evaluate how well rebuttals address reasons"
            ),
            SummativeAssessmentMoment(
                moment_name="Closing Statements",
                purpose="Summarize key points and final thoughts",
                typical_timing="End of debate",
                assessment_focus=["Organization", "Persuasiveness"],
                rubric_guidance="Assess summary clarity and impact"
            ),
            SummativeAssessmentMoment(
                moment_name="Reflection Review",
                purpose="Evaluate depth of student reflections",
                typical_timing="After debate",
                assessment_focus=["Insight", "Connection to skills"],
                rubric_guidance="Assess how well students articulate learning"
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="Plus/Delta",
                purpose="Identify what worked and what to improve",
                structure=[
                    "Plus: What went well?",
                    "Delta: What could we change?"
                ],
                timing_guidance="After debate",
                facilitation_notes="Use chart paper for group sharing"
            ),
            ReflectionProtocol(
                protocol_name="I Heard…",
                purpose="Practice active listening and summarizing",
                structure=[
                    "I heard you say…",
                    "Can you clarify?",
                    "Thank you for listening to me."
                ],
                timing_guidance="After each round",
                facilitation_notes="Model sentence stems first"
            )
        ],
        portfolio_guidance=(
            "Keep pro/con charts, speech notes, feedback forms, and reflections in one folder."
        )
    ),
    
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teacher",
            "Other grade-level classes",
            "Family at home"
        ],
        engagement_formats=[
            "Live classroom debate",
            "Poster display of pro/con charts",
            "Short video of debate highlights"
        ],
        preparation_requirements=[
            "Practice timing with a timer",
            "Check reason charts for accuracy",
            "Ensure respectful language"
        ],
        logistical_considerations=[
            "Arrange seating in debate format",
            "Set clear speaking order",
            "Provide timers"
        ]
    ),
    
    project_management_tools=[
        "Debate topic chart",
        "Pro/con reason organizer",
        "Speech planning sheets",
        "Debate schedule and roles chart",
        "Feedback and reflection forms"
    ],
    
    recommended_resources=[
        "Kid-friendly articles or books on debate topics",
        "Videos of children’s debates",
        "Sentence stems for opinions",
        "Graphic organizers (T-charts)",
        "Debate timer apps or egg timers"
    ],
    
    technology_suggestions=[
        "Screen or board for pro/con display",
        "Recording device for practice",
        "Digital slide tool for opening statements"
    ],
    
    standards_alignment_examples={
        "english_language_arts": [
            "CCSS.ELA-LITERACY.SL.3.1: Engage effectively in a range of collaborative discussions.",
            "CCSS.ELA-LITERACY.W.3.1: Write opinion pieces supporting a point of view."
        ],
        "social_studies": [
            "C3 D4.6.K-2: Identify strategies people can use to resolve conflicts peacefully."
        ],
        "cross_curricular": [
            "Critical thinking and decision making",
            "Listening and speaking",
            "Civic literacy"
        ]
    },
    
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge=(
            "Students evaluate reasons on both sides and construct clear arguments."
        ),
        authenticity="Debate real classroom or community questions.",
        public_product="A live debate or video recording shared with others.",
        collaboration="Work in teams of 2–3 to prepare arguments.",
        project_management="Timeline with research, practice, and debate phases.",
        reflection="Ongoing check-ins on listening and argument quality."
    ),
    
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN],
        social_structure_compatible=[SocialStructure.COLLABORATIVE, SocialStructure.NETWORKED],
        cognitive_complexity_range=[CognitiveComplexity.ANALYSIS, CognitiveComplexity.EVALUATION],
        authenticity_compatible=[AuthenticityLevel.APPLIED, AuthenticityLevel.IMPACT],
        scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED],
        product_complexity_compatible=[ProductComplexity.EXPERIENCE, ProductComplexity.SYSTEM],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.SYNCHRONOUS_REMOTE]
    ),
    
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we already think about our question?",
            "What reasons have we heard before?"
        ],
        what_we_wonder_prompts=[
            "Why would someone disagree?",
            "What examples support each side?"
        ],
        what_we_want_to_learn_prompts=[
            "Which side has stronger evidence?",
            "How can we find good examples?"
        ],
        how_we_might_explore_options=[
            "Read a short article or watch a video",
            "Interview classmates or family",
            "Brainstorm examples together"
        ],
        reflection_return_prompts=[
            "How did our thinking change?",
            "What new questions do we have?"
        ]
    ),
    
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Debate corner with pro/con boards",
            "Listening station with headphones for recordings",
            "Reflection nook with journals"
        ],
        documentation_displays=[
            "Pro/con charts on walls",
            "Speech notes pinned up",
            "Reflection boards"
        ],
        material_provocations=[
            "Sample debate topics",
            "Sentence starter cards",
            "Timer and bell"
        ],
        collaboration_zones=[
            "Team planning tables",
            "Audience seating area"
        ],
        reflection_retreats=[
            "Quiet writing spot",
            "Talking circle area"
        ]
    ),
    
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Pick a question to debate",
            "Choose a side or topic angle",
            "Select resources to research",
            "Decide your speaking role"
        ],
        voice_amplification_strategies=[
            "Students lead opening questions",
            "Peers provide structured feedback"
        ],
        ownership_transfer_milestones=[
            "Write and refine own speech notes",
            "Manage debate practice sessions"
        ],
        peer_collaboration_structures=[
            "Buddy research teams",
            "Peer feedback circles"
        ]
    ),
    
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Collect pro/con lists",
            "Record practice sessions",
            "Save speech drafts"
        ],
        student_thinking_artifacts=[
            "Reason charts",
            "Speech scripts",
            "Feedback forms"
        ],
        process_documentation_methods=[
            "Digital folder or binder",
            "Photo journal of debate day"
        ],
        celebration_sharing_formats=[
            "Class showcase debate",
            "Video highlights presentation"
        ]
    ),
    
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Design pro/con posters",
            "Create a visual mind map of reasons"
        ],
        kinesthetic_expression_options=[
            "Role-play debate motions",
            "Use body language to show agreement/disagreement"
        ],
        verbal_expression_options=[
            "Deliver opening and closing statements",
            "Practice impromptu rebuttals"
        ],
        collaborative_expression_options=[
            "Team debate format",
            "Peer feedback dialogues"
        ],
        creative_expression_options=[
            "Write a short debate comic strip",
            "Compose a chant summarizing key reasons"
        ]
    ),
    
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "New evidence changes our stance",
            "Teams need more practice time",
            "Students feel shy speaking aloud"
        ],
        student_interest_amplifiers=[
            "Let students pick their own topics",
            "Offer fun props or costumes"
        ],
        unexpected_connection_bridges=[
            "Link debate topic to current events",
            "Connect arguments to stories or books"
        ],
        community_opportunity_integrators=[
            "Invite another class to watch",
            "Share recordings with families"
        ]
    ),
    
    getting_started_essentials=[
        "Pick 2–3 fun debate questions",
        "Gather materials for pro/con charts",
        "Set up speaking area with timer"
    ],
    when_things_go_wrong=[
        "No reasons found: provide example reasons",
        "Interruptions happen: teach hand-raising",
        "Shy speakers: offer practice scripts"
    ],
    success_indicators=[
        "Students state clear reasons",
        "Debaters listen respectfully",
        "Evidence used in arguments",
        "Reflections show learning"
    ],
    teacher_preparation_notes=[
        "Prepare sample pro/con chart",
        "Model respectful language",
        "Arrange seating for debate format"
    ],
    common_challenges=[
        "Talking over each other",
        "Reasons too vague",
        "Difficulty listening quietly",
        "Stage fright"
    ],
    teacher_prep_essentials=[
        "Print pro/con graphic organizers",
        "Prepare sentence stems cards",
        "Set up timer and speaking order"
    ],
    student_readiness="Best for grades 3–7 who can speak in full sentences and listen to peers.",
    community_engagement_level="Low – in-class activity with possible family viewing.",
    assessment_highlights=[
        "Strength and clarity of reasons",
        "Quality of rebuttals",
        "Listening and response skills",
        "Depth of reflection"
    ],
    assessment_focus="Skills in reasoning, speaking, listening, and respect.",
    what_success_looks_like="Students share strong reasons, listen well, and reflect on differing views.",
    final_product_description="A brief class debate with opening statements, rebuttals, and a reflection session.",
    
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Argumentation & Reasoning",
            application="Students gather reasons and use evidence to support their side.",
            assessment_connection="Assessed via clarity and relevance of reasons."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Public Speaking",
            application="Students deliver statements clearly and confidently.",
            assessment_connection="Assessed via volume, clarity, and organization."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Active Listening & Respect",
            application="Students listen to others and respond politely.",
            assessment_connection="Assessed via quality of rebuttals and peer feedback."
        )
    ]
)
