# templates/integration_skill/skill_application.py

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

TEMPLATE = create_skill_application_template = BaseTemplate(
    template_id="skill_application",
    intent=TemplateIntent.SKILL_APPLICATION,
    display_name="Skill Application Project",
    description=(
        "Students choose a practical skill—like measuring ingredients, telling time, "
        "or following directions—and apply it in a fun, real-world challenge."
    ),
    pedagogical_approach="Experiential, hands-on learning through authentic practice",
    comprehensive_overview=(
        "In this project, students pick a concrete skill to master. They start by "
        "exploring why the skill matters, practice it in guided activities, plan a challenge "
        "that uses the skill—such as cooking a simple recipe, creating a schedule, or "
        "building a mini-guide—carry out their plan, and then reflect on how well they did and how "
        "to improve. This builds confidence and shows how school skills help in everyday life."
    ),
    driving_question_template="How can we use [skill] to [complete a real task] in our world?",
    
    core_learning_cycle=[
        "Explore & Practice",
        "Plan Application",
        "Execute & Observe",
        "Assess & Improve",
        "Share & Reflect"
    ],
    
    essential_skills=[
        "skill_practice",
        "planning",
        "execution",
        "self_assessment",
        "reflection",
        "communication"
    ],
    
    required_components=[
        "driving_question",
        "practice_log",
        "application_plan",
        "completed_task_artifact",
        "self_assessment_notes",
        "reflection_entry"
    ],
    
    natural_subject_areas=[
        SubjectArea.MATHEMATICS,
        SubjectArea.HEALTH,
        SubjectArea.ART,
        SubjectArea.ENGLISH_LANGUAGE_ARTS
    ],
    
    cross_curricular_connections=[
        "Reading instructions or recipes",
        "Measuring and math in real contexts",
        "Writing steps and notes",
        "Speaking or presenting outcomes",
        "Teamwork and collaboration"
    ],
    
    entry_event_framework=EntryEventFramework(
        purpose="Spark interest by showing a real-life example of the skill in action",
        design_principles=[
            "Keep it concrete and visual",
            "Use relatable, everyday contexts",
            "Encourage ‘I wonder…’ questions",
            "Connect to students’ lives"
        ],
        template_options=[
            EntryEventOption(
                type="show_and_try",
                example="Demonstrate using a measuring cup to pour water, then let students try simple pours.",
                student_response_pattern="Watch → try → share what was easy or hard",
                question_generation_method="What do you notice? What questions do you have?",
                estimated_time="15 minutes",
                materials_needed=["Measuring cups", "Water, sand, or rice", "Containers"]
            ),
            EntryEventOption(
                type="story_problem",
                example="Tell a short story about cooking pancakes to prompt planning ingredients and steps.",
                student_response_pattern="Listen → draw the steps → discuss in pairs",
                question_generation_method="What steps matter most? What could go wrong?",
                estimated_time="20 minutes",
                materials_needed=["Story script", "Paper and pencils"]
            )
        ],
        customization_guidance="Pick an entry event that showcases the skill clearly and engages students"
    ),
    
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Explore & Practice",
            learning_purpose="Get comfortable with the basic steps of the skill",
            core_activities=[
                "Model the skill as a class",
                "Practice in pairs or small groups",
                "Record successes and challenges"
            ],
            essential_deliverables=[
                "Practice log with 3–5 entries",
                "Notes on what went well and what was tricky"
            ],
            reflection_checkpoints=[
                "Which part felt easiest?",
                "What part needs more practice?"
            ],
            duration_scaling_notes="Sprint: 1 practice round; Unit: 3–5 rounds; Journey: 5+ rounds"
        ),
        MilestoneTemplate(
            milestone_name="Plan Application",
            learning_purpose="Design a simple task that uses the skill in a meaningful way",
            core_activities=[
                "Brainstorm real tasks (e.g., simple recipe, schedule)",
                "Outline steps and needed materials",
                "Assign roles if working in teams"
            ],
            essential_deliverables=[
                "Written application plan",
                "Materials checklist"
            ],
            reflection_checkpoints=[
                "Is our plan clear?",
                "Do we have everything we need?"
            ],
            duration_scaling_notes="Sprint: Outline only; Unit: Detailed plan; Journey: Add backup options"
        ),
        MilestoneTemplate(
            milestone_name="Execute & Observe",
            learning_purpose="Carry out the plan and observe outcomes carefully",
            core_activities=[
                "Follow plan steps one by one",
                "Document progress (photos, notes)",
                "Note any surprises or mistakes"
            ],
            essential_deliverables=[
                "Completed task artifact (e.g., cooked item, drawn schedule)",
                "Observation notes"
            ],
            reflection_checkpoints=[
                "What went according to plan?",
                "What did we need to adjust?"
            ],
            duration_scaling_notes="Same process; adjust depth by duration"
        ),
        MilestoneTemplate(
            milestone_name="Assess & Improve",
            learning_purpose="Evaluate how well we applied the skill and plan refinements",
            core_activities=[
                "Use a simple rubric or checklist to self-assess",
                "Discuss with peers or teacher",
                "Plan one change to improve"
            ],
            essential_deliverables=[
                "Self-assessment notes",
                "Improvement plan"
            ],
            reflection_checkpoints=[
                "How could we do it better next time?",
                "What did we learn about the skill?"
            ],
            duration_scaling_notes="Sprint: One tweak; Unit: Two tweaks; Journey: Multiple iterations"
        ),
        MilestoneTemplate(
            milestone_name="Share & Reflect",
            learning_purpose="Present our work and think about how the skill helps in real life",
            core_activities=[
                "Prepare a short demonstration or poster",
                "Share with classmates or family",
                "Write a final reflection"
            ],
            essential_deliverables=[
                "Presentation or visual display",
                "Final reflection journal"
            ],
            reflection_checkpoints=[
                "Why is this skill important?",
                "When might we use it again?"
            ],
            duration_scaling_notes="Same for all durations"
        )
    ],
    
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Practice Log Review",
                purpose="Check completeness of practice entries",
                implementation_guidance="Teacher reviews logs and gives feedback",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After practice",
                    Duration.JOURNEY: "Weekly",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Spot check",
                    Duration.UNIT: "Basic comments",
                    Duration.JOURNEY: "Detailed feedback",
                    Duration.CAMPAIGN: "Peer and teacher feedback"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Plan Check",
                purpose="Ensure application plan is clear and feasible",
                implementation_guidance="Peers review each other’s plans against a checklist",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After planning",
                    Duration.JOURNEY: "Mid-execution",
                    Duration.CAMPAIGN: "Bi-weekly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Thumbs up/down",
                    Duration.UNIT: "Verbal feedback",
                    Duration.JOURNEY: "Written notes",
                    Duration.CAMPAIGN: "Rubric-based review"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Self-Assessment Check",
                purpose="Support students using a simple rubric to reflect on their work",
                implementation_guidance="Students complete rubric and discuss with a partner",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After execution",
                    Duration.JOURNEY: "After each iteration",
                    Duration.CAMPAIGN: "Monthly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Simple smiley/frowny",
                    Duration.UNIT: "Discussion prompts",
                    Duration.JOURNEY: "Written reflections",
                    Duration.CAMPAIGN: "Portfolio entries"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Task Presentation",
                purpose="Show the completed artifact and explain steps",
                typical_timing="After execution phase",
                assessment_focus=["Accuracy", "Clarity of explanation"],
                rubric_guidance="Assess how well steps were followed and explained"
            ),
            SummativeAssessmentMoment(
                moment_name="Improvement Plan Share",
                purpose="Share how we would improve next time",
                typical_timing="After assessment phase",
                assessment_focus=["Insight", "Actionability"],
                rubric_guidance="Evaluate depth of improvement ideas"
            ),
            SummativeAssessmentMoment(
                moment_name="Final Reflection",
                purpose="Reflect on learning and real-life use of the skill",
                typical_timing="End of project",
                assessment_focus=["Depth of reflection", "Connection to real life"],
                rubric_guidance="Assess connection to daily contexts and self-awareness"
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="I Did / I Would",
                purpose="Identify what we did well and what we’d change",
                structure=[
                    "I did…",
                    "I would…"
                ],
                timing_guidance="After assessment",
                facilitation_notes="Use simple sentence stems"
            ),
            ReflectionProtocol(
                protocol_name="Plus/Delta",
                purpose="Note positives and areas for improvement",
                structure=[
                    "Plus: What went well?",
                    "Delta: What could we change?"
                ],
                timing_guidance="Final reflection",
                facilitation_notes="Record on chart paper"
            )
        ],
        portfolio_guidance=(
            "Keep practice logs, plans, artifacts, assessment rubrics, and reflections in one folder."
        )
    ),
    
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teacher",
            "Family members at home",
            "Other classrooms"
        ],
        engagement_formats=[
            "Live demonstration",
            "Poster or display board",
            "Digital slideshow"
        ],
        preparation_requirements=[
            "Practice your demonstration",
            "Check your artifacts and visuals",
            "Prepare talking points"
        ],
        logistical_considerations=[
            "Reserve presentation space",
            "Set clear time limits",
            "Invite audience"
        ]
    ),
    
    project_management_tools=[
        "Practice log template",
        "Application plan worksheet",
        "Materials checklist",
        "Rubric sheets",
        "Reflection journal"
    ],
    
    recommended_resources=[
        "Skill-specific tools (measuring cups, timers)",
        "Instructional picture books or videos",
        "Printable rubrics",
        "Chart paper and markers",
        "Digital presentation tools"
    ],
    
    technology_suggestions=[
        "Tablet or camera for recording demonstrations",
        "Interactive timers or apps",
        "Presentation software"
    ],
    
    standards_alignment_examples={
        "mathematics": [
            "CCSS.MATH.CONTENT.3.MD.A.1: Tell and write time to the nearest minute and measure intervals of time.",
            "CCSS.MATH.CONTENT.4.MD.B.4: Make a line plot to display a data set of measurements."
        ],
        "english_language_arts": [
            "CCSS.ELA-LITERACY.SL.3.4: Report on a topic with appropriate facts."
        ],
        "cross_curricular": [
            "21st century life skills",
            "Self-management and reflection"
        ]
    },
    
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge=(
            "Students plan and execute a real task, reflecting on each step."
        ),
        authenticity="Tasks mirror everyday activities students and families do.",
        public_product="A demonstration or display that shows the skill in action.",
        collaboration="Work individually or in pairs with peer support.",
        project_management="Clear plan with practice, execution, and reflection phases.",
        reflection="Ongoing self-assessment and group discussions."
    ),
    
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY],
        social_structure_compatible=[SocialStructure.INDIVIDUAL, SocialStructure.PEER_COLLABORATIVE],
        cognitive_complexity_range=[CognitiveComplexity.APPLICATION, CognitiveComplexity.EVALUATION],
        authenticity_compatible=[AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED],
        scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED],
        product_complexity_compatible=[ProductComplexity.EXPERIENCE, ProductComplexity.PORTFOLIO],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.SYNCHRONOUS_REMOTE]
    ),
    
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we already know about this skill?",
            "When have we used it before?"
        ],
        what_we_wonder_prompts=[
            "How can we use this skill to solve a problem?",
            "What steps will be hardest?"
        ],
        what_we_want_to_learn_prompts=[
            "What do we need to practice more?",
            "How will we measure success?"
        ],
        how_we_might_explore_options=[
            "Try the skill step by step",
            "Watch a demonstration video",
            "Interview someone who uses it"
        ],
        reflection_return_prompts=[
            "What surprised us about our performance?",
            "What will we do differently next time?"
        ]
    ),
    
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Practice stations with all materials",
            "Display area for artifacts",
            "Reflection corner with journals"
        ],
        documentation_displays=[
            "Practice logs on a wall",
            "Plans and checklists displayed",
            "Final artifacts showcased"
        ],
        material_provocations=[
            "Example artifacts or tools",
            "Visual step-by-step guides"
        ],
        collaboration_zones=[
            "Partner practice tables",
            "Peer assessment stations"
        ],
        reflection_retreats=[
            "Quiet writing space",
            "Talking circle area"
        ]
    ),
    
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Choose which skill to apply",
            "Decide on task complexity",
            "Select presentation format"
        ],
        voice_amplification_strategies=[
            "Students share practice tips",
            "Peer coaching opportunities"
        ],
        ownership_transfer_milestones=[
            "Write and follow own plan",
            "Lead peer practice sessions"
        ],
        peer_collaboration_structures=[
            "Buddy practice pairs",
            "Small group feedback"
        ]
    ),
    
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Photograph each practice session",
            "Collect annotated checklists",
            "Save final artifacts"
        ],
        student_thinking_artifacts=[
            "Practice logs",
            "Plans and checklists",
            "Assessment rubrics"
        ],
        process_documentation_methods=[
            "Binder or digital folder",
            "Photo journal"
        ],
        celebration_sharing_formats=[
            "Class showcase",
            "Family demo night"
        ]
    ),
    
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Draw step-by-step diagrams",
            "Create how-to posters"
        ],
        kinesthetic_expression_options=[
            "Act out the process",
            "Use role-play to demonstrate steps"
        ],
        verbal_expression_options=[
            "Explain each step aloud",
            "Record a voice-over guide"
        ],
        collaborative_expression_options=[
            "Team demonstrations",
            "Peer interviews"
        ],
        creative_expression_options=[
            "Write a short guide booklet",
            "Compose a rhyming chant for steps"
        ]
    ),
    
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "Students get stuck on a step",
            "Tools are unfamiliar",
            "Task takes longer than expected"
        ],
        student_interest_amplifiers=[
            "Offer fun variations or challenges",
            "Connect skill to favorite activities"
        ],
        unexpected_connection_bridges=[
            "Link skill to art or music",
            "Relate it to a story or game"
        ],
        community_opportunity_integrators=[
            "Invite a family member to demonstrate",
            "Share at a school assembly"
        ]
    ),
    
    getting_started_essentials=[
        "Choose a clear, age-appropriate skill",
        "Gather all practice materials",
        "Prepare example artifacts or videos"
    ],
    
    when_things_go_wrong=[
        "Practice logs missing: model logging",
        "Steps out of order: use visual guides",
        "Task too hard: simplify steps"
    ],
    
    success_indicators=[
        "Students follow each step correctly",
        "Artifacts meet the task goal",
        "Reflections show learning and growth"
    ],
    
    teacher_preparation_notes=[
        "Model the full process before students try",
        "Prepare clear visual guides and examples",
        "Organize materials by station"
    ],
    
    common_challenges=[
        "Skipping steps or rushing",
        "Losing track of tools or materials",
        "Difficulty assessing own work",
        "Presentation nerves"
    ],
    
    teacher_prep_essentials=[
        "Print practice log and plan templates",
        "Gather demonstration materials",
        "Set up practice and demo spaces"
    ],
    
    student_readiness="Ideal for grades 3–7 who can follow multi-step instructions with guidance.",
    
    community_engagement_level="Low – classroom based, with optional family or school showcase.",
    
    assessment_highlights=[
        "Accuracy of task execution",
        "Clarity of self-assessment",
        "Depth of reflection"
    ],
    
    assessment_focus="Skills in planning, execution, self-assessment, and reflection.",
    
    what_success_looks_like="Students complete the task successfully, assess their work, and reflect on next steps.",
    
    final_product_description="A demonstrated artifact or process guide, accompanied by logs and reflections.",
    
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Planning & Organization",
            application="Students break down tasks and gather materials.",
            assessment_connection="Assessed via clarity of plan and readiness."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Execution & Precision",
            application="Students follow steps accurately and carefully.",
            assessment_connection="Assessed via correctness and neatness of the artifact."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Self-Assessment & Reflection",
            application="Students use rubrics to evaluate and improve their work.",
            assessment_connection="Assessed via depth of reflection and improvement plan."
        )
    ]
)
