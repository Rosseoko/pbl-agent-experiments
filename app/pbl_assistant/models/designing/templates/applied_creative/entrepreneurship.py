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

TEMPLATE = create_entrepreneurship_template = BaseTemplate(
    template_id="entrepreneurship",
    intent=TemplateIntent.ENTREPRENEURSHIP,
    display_name="Entrepreneurship Project",
    description="Students identify real-world problems or opportunities and develop sustainable, viable ventures to address them.",
    pedagogical_approach="Lean startup–informed PBL combining design thinking, market research, and iterative prototyping.",
    comprehensive_overview="""
The Entrepreneurship Project guides learners through the full venture creation cycle: opportunity identification, business model development, prototype/MVP creation, customer validation, and pitching for buy-in. Students work in teams to research markets, test assumptions with real users, refine their offerings, and present a compelling pitch to authentic audiences. Through this process, they gain skills in problem solving, financial literacy, marketing, and strategic planning.
""",
    driving_question_template="How might we [solve a real-world problem or seize an opportunity] through a sustainable and viable entrepreneurial venture?",
    core_learning_cycle=[
        "Opportunity Identification",
        "Ideation & Business Modeling",
        "Prototype & MVP Development",
        "Market Testing & Feedback",
        "Pitch & Reflection"
    ],
    essential_skills=[
        "market_research",
        "ideation",
        "business_modeling",
        "financial_planning",
        "marketing",
        "pitching",
        "critical_reflection"
    ],
    required_components=[
        "problem_or_opportunity_statement",
        "business_model_canvas",
        "prototype_or_mvp",
        "customer_interviews",
        "marketing_plan",
        "pitch_deck",
        "process_reflection"
    ],
    natural_subject_areas=[
        SubjectArea.SOCIAL_STUDIES,
        SubjectArea.MATHEMATICS,
        SubjectArea.ENGLISH_LANGUAGE_ARTS
    ],
    cross_curricular_connections=[
        "Basic accounting and finance",
        "Entrepreneurial case studies",
        "Marketing and communication",
        "Economics and social impact",
        "Technology integration for prototyping"
    ],
    entry_event_framework=EntryEventFramework(
        purpose="Introduce entrepreneurial mindset and real-world business challenges.",
        design_principles=[
            "Engage with authentic market problems",
            "Highlight successful ventures and failures",
            "Promote inquiry and curiosity",
            "Connect to student interests and experiences"
        ],
        template_options=[
            EntryEventOption(
                type="shark_tank_analysis",
                example="Watch and analyze Shark Tank pitch excerpts",
                student_response_pattern="Observe → Critique → Group discussion",
                question_generation_method="What made a pitch compelling or weak?",
                estimated_time="45 minutes",
                materials_needed=["Video clips", "Pitch evaluation rubric"]
            ),
            EntryEventOption(
                type="local_business_visit",
                example="Interview a local entrepreneur about their journey",
                student_response_pattern="Plan questions → Conduct interview → Synthesize insights",
                question_generation_method="What challenges and successes did they encounter?",
                estimated_time="60 minutes",
                materials_needed=["Interview guides", "Recording device"]
            )
        ],
        customization_guidance="Choose an entry event that best aligns with community and student contexts."
    ),
    milestone_templates=[
        MilestoneTemplate(
            milestone_name="Opportunity Identification",
            learning_purpose="Define a clear problem or opportunity and research its context.",
            core_activities=[
                "Problem framing and stakeholder mapping",
                "Preliminary market research",
                "Customer empathy interviews",
                "Opportunity statement drafting"
            ],
            essential_deliverables=[
                "Problem/opportunity statement",
                "Stakeholder analysis",
                "Interview summaries"
            ],
            reflection_checkpoints=[
                "Whose needs are we addressing?",
                "What evidence supports this opportunity?",
                "How might this evolve?"
            ],
            duration_scaling_notes="Sprint: Single customer persona; Unit: Two interviews; Journey: Multiple segments."
        ),
        MilestoneTemplate(
            milestone_name="Ideation & Business Modeling",
            learning_purpose="Generate solutions and build a sustainable business model.",
            core_activities=[
                "Brainstorming solution ideas",
                "Business Model Canvas creation",
                "Value proposition design",
                "Feedback from peers and mentors"
            ],
            essential_deliverables=[
                "Business Model Canvas",
                "Value Proposition Canvas",
                "Feedback log"
            ],
            reflection_checkpoints=[
                "What assumptions are we making?",
                "How sustainable is our model?",
                "What risks need mitigation?"
            ],
            duration_scaling_notes="Sprint: Canvas sketch; Unit: Canvas with annotated risks; Journey: Detailed model with cost analysis."
        ),
        MilestoneTemplate(
            milestone_name="Prototype & MVP Development",
            learning_purpose="Build and test a minimum viable product or service.",
            core_activities=[
                "Low-fidelity prototyping",
                "MVP creation",
                "Usability testing sessions",
                "Iteration planning"
            ],
            essential_deliverables=[
                "Prototype or MVP",
                "Test feedback",
                "Iteration plan"
            ],
            reflection_checkpoints=[
                "What worked in our MVP?",
                "What did users struggle with?",
                "How will we improve?"
            ],
            duration_scaling_notes="Sprint: Paper prototype; Unit: Functional MVP; Journey: Customer-ready version."
        ),
        MilestoneTemplate(
            milestone_name="Market Testing & Feedback",
            learning_purpose="Gather real customer feedback and refine the venture.",
            core_activities=[
                "Customer interviews and surveys",
                "Data analysis of feedback",
                "Business model adjustments",
                "Pivot or persevere decisions"
            ],
            essential_deliverables=[
                "Customer feedback report",
                "Revised business model",
                "Pivot/persevere record"
            ],
            reflection_checkpoints=[
                "What surprising insights emerged?",
                "How has our model changed?",
                "What next steps are critical?"
            ],
            duration_scaling_notes="Sprint: One survey; Unit: Multiple interviews; Journey: Longitudinal testing."
        ),
        MilestoneTemplate(
            milestone_name="Pitch & Reflection",
            learning_purpose="Develop and deliver a compelling pitch and reflect on the entrepreneurial journey.",
            core_activities=[
                "Pitch deck preparation",
                "Rehearsal and feedback",
                "Pitch event to authentic audience",
                "Process reflection"
            ],
            essential_deliverables=[
                "Pitch deck",
                "Presentation recording",
                "Reflection journal"
            ],
            reflection_checkpoints=[
                "How compelling was our narrative?",
                "What feedback influenced us most?",
                "How can we apply these lessons beyond?"
            ],
            duration_scaling_notes="All durations include pitch; depth of reflection scales with project length."
        )
    ],
    assessment_framework=AssessmentFramework(
        formative_tools=[
            FormativeAssessmentTool(
                tool_name="Business Model Journals",
                purpose="Document evolving business model and assumptions.",
                implementation_guidance="Maintain dated entries of model updates and learnings.",
                frequency_recommendations={
                    Duration.SPRINT: "Daily entries",
                    Duration.UNIT: "After each milestone",
                    Duration.JOURNEY: "Weekly summaries",
                    Duration.CAMPAIGN: "Bi-weekly business reports"
                },
                scaling_guidance={
                    Duration.SPRINT: "Canvas sketches",
                    Duration.UNIT: "Annotated canvases",
                    Duration.JOURNEY: "Professional documentation",
                    Duration.CAMPAIGN: "Executive summaries"
                }
            ),
            FormativeAssessmentTool(
                tool_name="Customer Interview Reflections",
                purpose="Process and synthesize customer feedback.",
                implementation_guidance="Structured reflection after each interview.",
                frequency_recommendations={
                    Duration.SPRINT: "Not applicable",
                    Duration.UNIT: "After each interview",
                    Duration.JOURNEY: "After interviews and weekly reviews",
                    Duration.CAMPAIGN: "After each major testing cycle"
                },
                scaling_guidance={
                    Duration.SPRINT: "Basic notes",
                    Duration.UNIT: "Detailed summaries",
                    Duration.JOURNEY: "Comprehensive analysis",
                    Duration.CAMPAIGN: "Professional research report"
                }
            )
        ],
        summative_moments=[
            SummativeAssessmentMoment(
                moment_name="Business Model Presentation",
                purpose="Present and critique your business model.",
                typical_timing="Mid-project",
                assessment_focus=["Innovation", "Feasibility", "Market fit"],
                rubric_guidance="Evaluate creativity, viability, and customer alignment."
            ),
            SummativeAssessmentMoment(
                moment_name="Final Pitch",
                purpose="Deliver a polished pitch to authentic audience.",
                typical_timing="Project conclusion",
                assessment_focus=["Clarity", "Persuasiveness", "Professionalism"],
                rubric_guidance="Assess narrative strength, visual quality, and delivery."
            )
        ],
        reflection_protocols=[
            ReflectionProtocol(
                protocol_name="Entrepreneurial Reflection",
                purpose="Reflect on decisions, pivots, and learnings throughout.",
                structure=[
                    "What were our biggest assumptions?",
                    "How did feedback shift our approach?",
                    "What would we do differently next time?"
                ],
                timing_guidance="After final pitch",
                facilitation_notes="Use guided discussion or written prompts."
            )
        ],
        portfolio_guidance="Students compile business model canvases, customer reports, prototypes, and pitch decks."
    ),
    authentic_audience_framework=AuthenticAudienceFramework(
        audience_categories=[
            "Local entrepreneurs and mentors",
            "Potential customers",
            "Investors or school leaders",
            "Community stakeholders"
        ],
        engagement_formats=[
            "Pitch competition",
            "Prototype demonstration fair",
            "Business storyboard exhibition"
        ],
        preparation_requirements=[
            "Pitch deck and materials",
            "Prototype display setup",
            "Evaluation rubric for audience"
        ],
        logistical_considerations=[
            "Venue coordination",
            "Audience invitations",
            "Technical equipment"
        ]
    ),
    project_management_tools=[
        "Business Model Canvas template",
        "Interview scheduling calendar",
        "Prototype development timeline",
        "Pitch deck template"
    ],
    recommended_resources=[
        "Entrepreneurship case study library",
        "Business model guides",
        "Local business associations",
        "Financial projection templates"
    ],
    technology_suggestions=[
        "Business modeling software",
        "Prototype design tools",
        "Survey platforms",
        "Presentation software"
    ],
    standards_alignment_examples={
        "english_language_arts": [
            "CCSS.ELA-LITERACY.W.9-10.1: Write arguments to support claims with clear reasons and relevant evidence."
        ],
        "mathematics": [
            "CCSS.MATH.CONTENT.HSN.Q.A.1: Use units as a way to understand problems and guide solutions." 
        ],
        "social_studies": [
            "NCSS.D2.Eco.1.9-12: Explain how economic decision making affects individuals and societies." 
        ]
    },
    hqpbl_alignment=HQPBLAlignment(
        intellectual_challenge="Students engage in complex problem solving to develop viable business solutions.",
        authenticity="Real-world entrepreneurial context with genuine market validation.",
        public_product="Pitch to authentic audiences such as mentors and investors.",
        collaboration="Team-based collaboration across functional roles.",
        project_management="Multi-phase timeline with iterative feedback and pivots.",
        reflection="Ongoing reflection on entrepreneurial decisions and learnings."
    ),
    compatibility_matrix=CompatibilityMatrix(
        duration_compatible=[
            Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN
        ],
        social_structure_compatible=[
            SocialStructure.COLLABORATIVE, SocialStructure.NETWORKED
        ],
        cognitive_complexity_range=[
            CognitiveComplexity.ANALYSIS, CognitiveComplexity.SYNTHESIS, CognitiveComplexity.EVALUATION
        ],
        authenticity_compatible=[
            AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED, AuthenticityLevel.IMPACT
        ],
        scaffolding_compatible=[
            ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.MENTORED
        ],
        product_complexity_compatible=[
            ProductComplexity.PORTFOLIO, ProductComplexity.SYSTEM, ProductComplexity.EXPERIENCE
        ],
        delivery_mode_compatible=[
            DeliveryMode.FACE_TO_FACE, DeliveryMode.HYBRID, DeliveryMode.SYNCHRONOUS_REMOTE
        ]
    ),
    inquiry_framework=InquiryFramework(
        what_we_know_prompts=[
            "What businesses or services interest you?",
            "What problems do you see in your community or daily life?"
        ],
        what_we_wonder_prompts=[
            "What unmet needs exist for our target audience?",
            "How do successful entrepreneurs identify opportunities?"
        ],
        what_we_want_to_learn_prompts=[
            "How do we validate a business idea with customers?",
            "What costs and revenues should we consider?"
        ],
        how_we_might_explore_options=[
            "Conduct customer interviews or surveys",
            "Analyze competitor offerings",
            "Prototype low-fidelity MVPs"
        ],
        reflection_return_prompts=[
            "What did we learn from our customer feedback?",
            "How did our business model evolve?"
        ]
    ),
    learning_environment_framework=LearningEnvironmentFramework(
        physical_space_invitations=[
            "Innovation lab with prototyping tools",
            "Market research station with survey tablets",
            "Collaboration pods with whiteboards"
        ],
        documentation_displays=[
            "Business Model Canvas wall",
            "Customer feedback boards",
            "Prototype showcase area"
        ],
        material_provocations=[
            "Market trend reports",
            "Entrepreneurship case studies",
            "Prototyping tool demos"
        ],
        collaboration_zones=[
            "Team brainstorming pods",
            "Pitch rehearsal stage"
        ],
        reflection_retreats=[
            "Quiet analysis corner",
            "Financial planning cubicle"
        ]
    ),
    student_agency_framework=StudentAgencyFramework(
        natural_choice_points=[
            "Choose target market and focus",
            "Select prototyping tools",
            "Decide marketing strategies"
        ],
        voice_amplification_strategies=[
            "Student-led investor panels",
            "Peer mentoring for pitch practice"
        ],
        ownership_transfer_milestones=[
            "Teams self-manage customer interviews",
            "Students independently iterate prototypes"
        ],
        peer_collaboration_structures=[
            "Role-based teamwork (CEO, CFO, CMO)",
            "Cross-team pitch feedback sessions"
        ]
    ),
    documentation_framework=DocumentationFramework(
        learning_capture_opportunities=[
            "Business model canvas snapshots",
            "Interview transcript logs",
            "Prototype iteration records"
        ],
        student_thinking_artifacts=[
            "Idea generation mind maps",
            "Financial projection spreadsheets"
        ],
        process_documentation_methods=[
            "Pivot logs",
            "Annotated MVP versions"
        ],
        celebration_sharing_formats=[
            "Startup expo",
            "Pitch demo day"
        ]
    ),
    expression_pathways=ExpressionPathways(
        visual_expression_options=[
            "Infographics of business model",
            "Prototype display visuals"
        ],
        kinesthetic_expression_options=[
            "Role-play customer interactions"
        ],
        verbal_expression_options=[
            "Elevator pitches",
            "Storytelling presentations"
        ],
        collaborative_expression_options=[
            "Team pitch rehearsals"
        ],
        creative_expression_options=[
            "Branding and packaging design"
        ]
    ),
    emergent_learning_support=EmergentLearningSupport(
        pivot_opportunity_indicators=[
            "When customer feedback contradicts assumptions",
            "When prototype fails key functionality"
        ],
        student_interest_amplifiers=[
            "Allow exploration of alternative business ideas",
            "Provide mentor office hours"
        ],
        unexpected_connection_bridges=[
            "Link market research to design improvements",
            "Connect financial planning to resource constraints"
        ],
        community_opportunity_integrators=[
            "Introduce local business mentors",
            "Organize community focus groups"
        ]
    ),
    teacher_preparation_notes=[
        "Identify local business partners for interviews",
        "Prepare business model canvas templates",
        "Review lean startup methodology resources",
        "Set up prototyping materials and digital tools"
    ],
    common_challenges=[
        "Students struggle to define clear value propositions",
        "Difficulty balancing innovation with feasibility",
        "Managing limited resources and budgets",
        "Coordinating customer interview logistics",
        "Handling critical feedback constructively"
    ],
    getting_started_essentials=[
        "Gather business model canvas templates",
        "Arrange initial market research resources",
        "Form diverse teams"
    ],
    when_things_go_wrong=[
        "If interviews yield no insights: revise questions",
        "If prototypes fail: simplify MVP scope"
    ],
    signs_of_success=[
        "Teams identify clear market opportunities",
        "Prototypes demonstrate key features",
        "Pitches are coherent and compelling"
    ],
    teacher_prep_essentials=[
        "Secure entrepreneur guest speakers",
        "Organize pitch event logistics",
        "Prepare financial projection tools"
    ],
    student_readiness="Best for students comfortable with open-ended problem solving and basic business concepts.",
    community_engagement_level="Moderate: customer interviews and pitch events.",
    assessment_highlights=[
        "Quality of business model",
        "Depth of customer insights",
        "Pitch effectiveness"
    ],
    assessment_focus="Entrepreneurial process, market validation, and presentation skills.",
    what_success_looks_like="Students develop viable business proposals and defend them with evidence.",
    final_product_description="A validated business plan, prototype, and pitch deck.",
    core_skills=[
        BaseTemplate.CoreSkill(
            skill_name="Business Model Development",
            application="Creating and iterating on a sustainable business model.",
            assessment_connection="Evaluated through canvas completeness and viability analysis."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Market Research",
            application="Gathering and synthesizing customer insights.",
            assessment_connection="Evaluated through interview summaries and feedback integration."
        ),
        BaseTemplate.CoreSkill(
            skill_name="Pitching & Communication",
            application="Crafting and delivering persuasive pitches.",
            assessment_connection="Evaluated through audience reception and rubric scores."
        )
    ]
)
