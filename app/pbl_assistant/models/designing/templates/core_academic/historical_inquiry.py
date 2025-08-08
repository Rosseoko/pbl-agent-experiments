# templates/core_academic/historical_inquiry.py

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

TEMPLATE = create_historical_inquiry_template = BaseTemplate(
    template_id="historical_inquiry",
    intent=TemplateIntent.HISTORICAL_INQUIRY,
    display_name="Historical Inquiry Project",
    description="Students become young historians: they ask questions about the past, find evidence, and share their discoveries.",
    pedagogical_approach="Inquiry-based learning through historical research and storytelling",
    comprehensive_overview=(
        "In this project, students pick a person, place, or event from history that interests them. "
        "They learn to ask good questions, find and read simple primary and secondary sources (like pictures, short texts, or videos), "
        "build a timeline or map, and then share what they learned with classmates or family. "
        "Along the way, they practice reading, writing, critical thinking, and speaking—just like real historians!"
    ),
    driving_question_template="What can we learn from [person/place/event] about life long ago?",
    
    core_learning_cycle=[
        "Ask Questions & Pick Topic",
        "Find & Read Sources",
        "Organize & Analyze Evidence",
        "Create & Share Report",
        "Reflect & Connect to Today"
    ],
    
    essential_skills=[
        "question_formulation",
        "source_analysis",
        "evidence_gathering",
        "timeline_construction",
        "writing_reports",
        "presentation_skills",
        "reflection"
    ],
    
    required_components=[
        "driving_question",
        "source_list",
        "timeline_or_map",
        "final_report_or_presentation",
        "reflection_note"
    ],
    
    natural_subject_areas=[
        SubjectArea.SOCIAL_STUDIES,
        SubjectArea.ENGLISH_LANGUAGE_ARTS
    ],
    
    cross_curricular_connections=[
        "Reading and summarizing texts",
        "Basic map and timeline skills",
        "Drawing or illustrating findings",
        "Writing clear sentences",
        "Speaking confidently to an audience"
    ],
    
    entry_event_framework=EntryEventFramework(
        purpose="Spark curiosity with a story, photo, or artifact",
        design_principles=[
            "Use real historical pictures or objects",
            "Tell a short, exciting story",
            "Ask open-ended ‘I wonder…’ questions",
            "Connect to students’ own lives"
        ],
        template_options=[
            EntryEventOption(
                type="artifact_show_and_tell",
                example="Bring in an old toy, tool, or photograph and ask: What can we guess about its time?",
                student_response_pattern="Observe → ask questions → discuss with partner",
                question_generation_method="What do you notice? What do you wonder about its story?",
                estimated_time="30 minutes",
                materials_needed=["Artifact or photo", "Sticky notes", "Question chart"]
            ),
            EntryEventOption(
                type="story_time",
                example="Read a short story about a local hero or event, then ask: What would you like to learn next?",
                student_response_pattern="Listen → write questions → share aloud",
                question_generation_method="What parts surprised you? What do you want to find out?",
                estimated_time="20 minutes",
                materials_needed=["Story book or printout", "Paper and pencils"]
            )
        ],
        customization_guidance="Choose the entry event that fits your classroom resources and student interests"
    ),
    
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Ask Questions & Plan",
            learning_purpose="Students pick a historical topic and write good research questions",
            core_activities=[
                "Brainstorm history topics",
                "Use question starters (Who? What? When? Where? Why? How?)",
                "Choose one topic and refine questions",
                "Plan simple research steps"
            ],
            essential_deliverables=[
                "List of 3–5 research questions",
                "Topic choice and why it matters",
                "Basic research plan"
            ],
            reflection_checkpoints=[
                "Which question is most exciting?",
                "What do we already know?",
                "What will we look for first?"
            ],
            duration_scaling_notes="Sprint: Pick topic & questions only; Unit: Add research plan; Journey: Add source gathering"
        ),
        MilestoneTemplate(
            milestone_name="Find & Read Sources",
            learning_purpose="Students gather simple sources and learn to read for key details",
            core_activities=[
                "Locate books, articles, or videos",
                "Use a source organizer to note facts",
                "Highlight important dates or names",
                "Discuss findings in pairs"
            ],
            essential_deliverables=[
                "Source list with 3–5 items",
                "Notes on each source",
                "Key facts highlighted"
            ],
            reflection_checkpoints=[
                "Which source helped most?",
                "What new facts did we learn?",
                "Whose story is missing?"
            ],
            duration_scaling_notes="Sprint: 1–2 sources; Unit: 3–5 sources; Journey: Include a simple primary source"
        ),
        MilestoneTemplate(
            milestone_name="Organize & Analyze Evidence",
            learning_purpose="Students sort facts into a timeline or map and look for patterns",
            core_activities=[
                "Create a simple timeline or map",
                "Group facts by theme or date",
                "Discuss patterns or surprises",
                "Adjust timeline/map as needed"
            ],
            essential_deliverables=[
                "Draft timeline or map",
                "Labeled key events or locations",
                "Analysis notes"
            ],
            reflection_checkpoints=[
                "What story does our timeline tell?",
                "Which events are most important?",
                "What questions remain?"
            ],
            duration_scaling_notes="Sprint: Draft timeline; Unit: Add detail; Journey: Refine and color-code"
        ),
        MilestoneTemplate(
            milestone_name="Create & Share Report",
            learning_purpose="Students write or present what they learned using evidence",
            core_activities=[
                "Write a short report or script",
                "Design simple visuals (drawings, slides)",
                "Practice reading or presenting",
                "Share with classmates or family"
            ],
            essential_deliverables=[
                "Final report or presentation slides",
                "Visual aids",
                "Rehearsal notes"
            ],
            reflection_checkpoints=[
                "How clear is our story?",
                "Did we use our best evidence?",
                "How did the audience react?"
            ],
            duration_scaling_notes="Sprint: Short verbal share; Unit: Poster or slides; Journey: Multi-page report"
        ),
        MilestoneTemplate(
            milestone_name="Reflect & Connect to Today",
            learning_purpose="Students think about why this history matters now",
            core_activities=[
                "Write or draw a reflection on relevance",
                "Discuss connections to modern life",
                "Share one action or question for the future"
            ],
            essential_deliverables=[
                "Reflection journal entry",
                "Class discussion summary",
                "Future question or action idea"
            ],
            reflection_checkpoints=[
                "Why does this topic matter today?",
                "What can we learn for our own lives?",
                "What new questions do we have?"
            ],
            duration_scaling_notes="Same for all durations, vary depth"
        )
    ],
    
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Question Log",
                purpose="Track growth of research questions",
                implementation_guidance="Students add new or revised questions as they go",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "After research",
                    Duration.JOURNEY: "Weekly updates",
                    Duration.CAMPAIGN: "Bi-weekly summaries"
                },
                scaling_guidance={
                    Duration.SPRINT: "Simple list",
                    Duration.UNIT: "Organized chart",
                    Duration.JOURNEY: "Detailed notebook",
                    Duration.CAMPAIGN: "Digital journal"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Source Notes Check",
                purpose="Ensure students read and note key facts",
                implementation_guidance="Teacher reviews source notes after each session",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "Once",
                    Duration.JOURNEY: "After each source",
                    Duration.CAMPAIGN: "Weekly check"
                },
                scaling_guidance={
                    Duration.SPRINT: "Spot check",
                    Duration.UNIT: "Basic review",
                    Duration.JOURNEY: "Detailed feedback",
                    Duration.CAMPAIGN: "Peer review included"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Timeline Draft Review",
                purpose="Check accuracy of timeline or map",
                implementation_guidance="Teacher and peers give feedback on draft",
                frequency_recommendations={
                    Duration.SPRINT: "Once",
                    Duration.UNIT: "Mid-project",
                    Duration.JOURNEY: "Bi-monthly",
                    Duration.CAMPAIGN: "Monthly"
                },
                scaling_guidance={
                    Duration.SPRINT: "Peer check",
                    Duration.UNIT: "Teacher review",
                    Duration.JOURNEY: "Expert review",
                    Duration.CAMPAIGN: "Community member input"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Source Report",
                purpose="Present findings from research sources",
                typical_timing="After source gathering",
                assessment_focus=["Completeness of sources", "Accuracy of notes"],
                rubric_guidance="Assess how students used facts and cited sources"
            ),
            SummativeAssessmentMoment(
                moment_name="Timeline Presentation",
                purpose="Share timeline or map and explain key events",
                typical_timing="After analysis phase",
                assessment_focus=["Clarity of timeline", "Connections made"],
                rubric_guidance="Evaluate organization and explanation of events"
            ),
            SummativeAssessmentMoment(
                moment_name="Final Report or Presentation",
                purpose="Show full understanding of topic to an audience",
                typical_timing="Project conclusion",
                assessment_focus=["Use of evidence", "Communication skills"],
                rubric_guidance="Assess story clarity, accuracy, and engagement"
            ),
            SummativeAssessmentMoment(
                moment_name="Reflection Essay",
                purpose="Explain why history matters today",
                typical_timing="After sharing",
                assessment_focus=["Depth of reflection", "Personal connection"],
                rubric_guidance="Evaluate insight and connection to modern life"
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="What Surprised Me",
                purpose="Notice unexpected facts or stories",
                structure=[
                    "Describe one surprising fact",
                    "Explain why it surprised you",
                    "What questions does it raise now?"
                ],
                timing_guidance="After analysis phase",
                facilitation_notes="Use a talking circle or journal"
            ),
            ReflectionProtocol(
                protocol_name="Why It Matters Now",
                purpose="Connect past learning to today’s world",
                structure=[
                    "State one way this topic relates to us",
                    "Give an example from your life or community",
                    "Suggest one thing we can do next"
                ],
                timing_guidance="Final reflection",
                facilitation_notes="Share in pairs before whole group"
            )
        ],
        portfolio_guidance=(
            "Keep a folder (or digital file) with your questions, notes, timeline, draft, and final work."
        )
    ),
    
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Classmates and teacher",
            "Family members at home",
            "Other classes in school"
        ],
        engagement_formats=[
            "Class presentation with visuals",
            "Poster display in hallway",
            "Create a short video story"
        ],
        preparation_requirements=[
            "Practice your talk",
            "Check your facts",
            "Make your visuals clear and colorful"
        ],
        logistical_considerations=[
            "Schedule a date and time",
            "Reserve display space",
            "Invite family or other classes"
        ]
    ),
    
    project_management_tools=[
        "Question chart or sticky-note wall",
        "Source list tracker",
        "Timeline planner poster",
        "Draft checklist",
        "Presentation rehearsal guide"
    ],
    
    recommended_resources=[
        "Child-friendly history books or articles",
        "Library archives or local museum visits",
        "Simple timeline apps or printable templates",
        "Historical videos for kids",
        "Map printouts or digital map tools"
    ],
    
    technology_suggestions=[
        "Tablet or computer for research",
        "Digital timeline tools (e.g., Tiki-Toki)",
        "Camera or audio recorder for interviews",
        "Presentation software (e.g., slides)",
        "Online graphic organizers"
    ],
    
    standards_alignment_examples={
        "social_studies": [
            "NCSS.D2.His.3.3-5: Generate questions about events in the past",
            "NCSS.D2.His.5.3-5: Explain how people’s choices influence events"
        ],
        "english_language_arts": [
            "CCSS.ELA-LITERACY.W.3.2: Write informative/explanatory texts",
            "CCSS.ELA-LITERACY.SL.4.4: Report on a topic with visual displays"
        ],
        "cross_curricular": [
            "Research and inquiry skills",
            "Timeline and map literacy",
            "Presentation and design skills"
        ]
    },
    
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge=(
            "Students develop deep questions, find real evidence, and build a story of the past."
        ),
        authenticity="Work with real sources (photos, maps, stories) from the past.",
        public_product="A clear timeline and presentation that teaches others.",
        collaboration="Work in pairs or small teams to research and share.",
        project_management="Simple plan with clear steps and check-ins.",
        reflection="Ongoing thinking about what history teaches us today."
    ),
    
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN],
        social_structure_compatible=[SocialStructure.INDIVIDUAL, SocialStructure.COLLABORATIVE],
        cognitive_complexity_range=[CognitiveComplexity.ANALYSIS, CognitiveComplexity.SYNTHESIS],
        authenticity_compatible=[AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED],
        scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED],
        product_complexity_compatible=[ProductComplexity.PORTFOLIO, ProductComplexity.EXPERIENCE],
        delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.SYNCHRONOUS_REMOTE]
    ),
    
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What do we already know about our chosen topic?",
            "What have adults told us about this event or person?",
            "What can we see in old photos or maps?"
        ],
        what_we_wonder_prompts=[
            "Why did this happen?",
            "Who was involved and why?",
            "What would life have been like then?"
        ],
        what_we_want_to_learn_prompts=[
            "How did people solve problems long ago?",
            "What did children do in that time?",
            "How did this event change things?"
        ],
        how_we_might_explore_options=[
            "Read a short book or article",
            "Look at pictures or maps",
            "Watch a kid-friendly video",
            "Interview a family member who knows history"
        ],
        reflection_return_prompts=[
            "How has our understanding grown?",
            "What surprised us most?",
            "What new questions do we have?"
        ]
    ),
    
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "History corner with photos and maps",
            "Timeline wall for adding events",
            "Source bookstore with simple texts",
            "Reflection nook with journals",
            "Display table for final products"
        ],
        documentation_displays=[
            "Timeline drafts with sticky notes",
            "Source summaries on chart paper",
            "Photo or map galleries",
            "Student reflection boards"
        ],
        material_provocations=[
            "Old postcards or letters",
            "Simple artifacts (tools, toys)",
            "Children’s history books",
            "Printed maps or timelines"
        ],
        collaboration_zones=[
            "Research stations for pairs",
            "Timeline-building tables",
            "Presentation practice corner"
        ],
        reflection_retreats=[
            "Quiet journaling space",
            "Discussion circle area"
        ]
    ),
    
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Pick a topic that excites you",
            "Choose which sources to explore",
            "Decide how to show your timeline",
            "Select your presentation format"
        ],
        voice_amplification_strategies=[
            "Students lead small group discussions",
            "Students ask questions to classmates",
            "Peer-sharing sessions"
        ],
        ownership_transfer_milestones=[
            "Write your own research questions",
            "Manage your source notebook",
            "Plan your own presentation rehearsal"
        ],
        peer_collaboration_structures=[
            "Buddy system for note-taking",
            "Team timeline building",
            "Peer feedback loops"
        ]
    ),
    
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Take photos of timeline work",
            "Record 'aha' moments in journals",
            "Collect drafts and notes"
        ],
        student_thinking_artifacts=[
            "Question lists",
            "Source note sheets",
            "Timeline drafts"
        ],
        process_documentation_methods=[
            "Notebook entries with dates",
            "Photo strips of work in progress"
        ],
        celebration_sharing_formats=[
            "Gallery walk of timelines",
            "Class showcase presentations"
        ]
    ),
    
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Draw a comic of key events",
            "Create an illustrated map",
            "Make a photo-storyboard"
        ],
        kinesthetic_expression_options=[
            "Act out a historical scene",
            "Build a simple model of a place",
            "Timeline hopscotch game"
        ],
        verbal_expression_options=[
            "Tell a story circle",
            "Record a mini podcast",
            "Explain your timeline to a friend"
        ],  
        collaborative_expression_options=[
            "Group poster creation",
            "Peer teaching stations"
        ],
        creative_expression_options=[
            "Write a short historical poem",
            "Compose a song about the past"
        ]
    ),
    
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "Students ask new questions not in the plan",
            "Source reading leads to surprises",
            "Timeline gaps appear"
        ],
        student_interest_amplifiers=[
            "Let students pick extra sources",
            "Offer “mystery box” artifacts to explore",
            "Encourage personal connections to family history"
        ],
        unexpected_connection_bridges=[
            "Link local history to personal stories",
            "Connect past events to current community"
        ],
        community_opportunity_integrators=[
            "Invite a local historian guest",
            "Plan a simple field trip to a museum"
        ]
    ),
    
    getting_started_essentials=[
        "Pick 2–3 history topics with students",
        "Gather simple source materials",
        "Set up a timeline or map workspace"
    ],
    when_things_go_wrong=[
        "Students can’t find sources: provide a storybook",
        "Questions are too broad: help narrow focus",
        "Timeline is confusing: model a sample"
    ],
    success_indicators=[
        "Students ask strong, focused questions",
        "Sources are used accurately in work",
        "Timelines clearly show key events",
        "Presentations engage classmates",
        "Reflections connect past to present"
    ],
    teacher_preparation_notes=[
        "Gather age-appropriate sources in advance",
        "Prepare question starters and templates",
        "Set clear examples of timelines or reports",
        "Arrange space for group work and displays"
    ],
    common_challenges=[
        "Students pick topics that are too big",
        "Difficulty reading primary sources",
        "Keeping timeline events in order",
        "Public speaking anxiety"
    ],
    teacher_prep_essentials=[
        "Find simple history books or videos",
        "Print timeline templates",
        "Prepare reflection question prompts"
    ],
    student_readiness="Works best for students in grades 3–7 who can work with pictures and short texts under guidance.",
    community_engagement_level="Low – activities happen mostly in class, with possible family sharing at home.",
    assessment_highlights=[
        "Use of evidence from sources",
        "Clarity and organization of timeline",
        "Quality of report or presentation"
    ],
    assessment_focus="Process skills in asking questions, gathering evidence, and communicating findings.",
    what_success_looks_like="Students create a clear timeline or map, share accurate stories, and reflect on why history matters.",
    final_product_description="A student-created historical report or presentation, complete with a timeline/map and evidence notes.",
    
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Historical Inquiry",
            application="Students generate and refine research questions about the past.",
            assessment_connection="Assessed via clarity and depth of questions."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Evidence Analysis",
            application="Students find, read, and note key facts from sources.",
            assessment_connection="Assessed via accuracy and use of evidence."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Communication",
            application="Students present findings in written or oral form.",
            assessment_connection="Assessed via organization and engagement of audience."
        )
    ]
)
