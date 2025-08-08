# templates/applied_creative/community_action.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
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


TEMPLATE = create_engineering_design_template =  BaseTemplate(
        template_id="engineering_design",
        intent=TemplateIntent.ENGINEERING_DESIGN,
        display_name="Engineering Design Project",
        description="Students identify real community problems and develop action plans for meaningful change",
        pedagogical_approach="Problem-based learning with authentic community engagement",
        comprehensive_overview="""The Creative Expression Project engages students as civic investigators and changemakers, starting with their own curiosities about community challenges and building toward authentic action.

Learning Journey: Students begin by wondering about problems they notice in their community, then dive deep through stakeholder interviews, data exploration, and collaborative research. They develop and test creative solutions with community feedback before presenting action plans to real audiences who can implement change.

Student Experience: This project honors multiple ways of learning and expressing ideas—from visual storytelling to hands-on prototyping to community dialogue facilitation. Students choose their focus areas, research methods, and presentation formats while building genuine relationships with community stakeholders.

Flexible Implementation: Scales from 3-day community problem explorations to semester-long impact initiatives. Works equally well with small collaborative teams or networked connections across multiple classrooms. Can adapt to any delivery mode while maintaining authentic community engagement.

The project transforms students from passive learners into active citizens who see themselves as capable of creating meaningful change in their communities.""",
        
        driving_question_template="How can we address [specific community problem] to create positive change in our community?",
        
        core_learning_cycle=[
            "Project Launch & Problem Identification",
            "Research & Stakeholder Analysis", 
            "Solution Development & Testing",
            "Action Planning & Implementation",
            "Reflection & Community Presentation"
        ],
        
        essential_skills=[
            "research_and_inquiry",
            "stakeholder_analysis", 
            "solution_design",
            "persuasive_communication",
            "civic_engagement",
            "project_management",
            "critical_thinking"
        ],
        
        required_components=[
            "authentic_community_problem",
            "stakeholder_engagement",
            "evidence_based_research", 
            "solution_prototyping",
            "community_presentation",
            "reflection_on_civic_process"
        ],
        
        natural_subject_areas=[
            SubjectArea.SOCIAL_STUDIES,
            SubjectArea.ENGLISH_LANGUAGE_ARTS,
            SubjectArea.MATHEMATICS
        ],
        
        cross_curricular_connections=[
            "Data analysis and statistics",
            "Research and writing skills",
            "Public speaking and presentation",
            "Digital literacy and media creation",
            "Ethics and civic responsibility"
        ],
        
        entry_event_framework=EntryEventFramework(
            purpose="Create emotional investment in community issues and generate authentic student questions",
            design_principles=[
                "Connect to students' lived experiences",
                "Present real community challenges",
                "Generate curiosity and questions",
                "Establish stakes and urgency"
            ],
            template_options=[
                EntryEventOption(
                    type="community_problem_gallery_walk",
                    example="Gallery walk of local news articles, photos, and data showing community challenges",
                    student_response_pattern="Silent observation → individual reflection → pair sharing → whole group discussion",
                    question_generation_method="What do you notice? What do you wonder? What do you care about?",
                    estimated_time="45 minutes",
                    materials_needed=["Local news articles", "Community photos", "Statistical data", "Sticky notes"]
                ),
                EntryEventOption(
                    type="community_stakeholder_panel",
                    example="Panel of community members (residents, officials, activists) sharing challenges",
                    student_response_pattern="Listen → question formulation → structured interview → synthesis",
                    question_generation_method="Based on stakeholder stories, what problems need solutions?",
                    estimated_time="60 minutes",
                    materials_needed=["Community stakeholder contacts", "Interview question stems", "Recording devices"]
                )
            ],
            customization_guidance="Select entry event based on available community connections and student interests"
        ),
        
        milestone_templates=[
            MilestoneTemplate(
                milestone_name="Project Launch & Problem Selection",
                learning_purpose="Establish team dynamics, select community problem focus, generate initial questions",
                core_activities=[
                    "Entry event engagement",
                    "Community problem exploration",
                    "Team formation and norming",
                    "Problem selection and justification",
                    "Initial research planning"
                ],
                essential_deliverables=[
                    "Team working agreements",
                    "Selected community problem statement", 
                    "Initial research questions",
                    "Project timeline and roles"
                ],
                reflection_checkpoints=[
                    "Why does this problem matter to our team?",
                    "What do we already know vs. need to learn?",
                    "How will we work together effectively?"
                ],
                duration_scaling_notes="Sprint: Focus on problem selection only. Unit: Add basic research planning. Journey/Campaign: Include comprehensive stakeholder mapping."
            ),
            
            MilestoneTemplate(
                milestone_name="Research & Stakeholder Analysis",
                learning_purpose="Develop deep understanding of problem through multiple perspectives and evidence",
                core_activities=[
                    "Primary source research methodology",
                    "Stakeholder identification and mapping",
                    "Interview planning and execution",
                    "Data collection and organization",
                    "Perspective analysis and synthesis"
                ],
                essential_deliverables=[
                    "Research methodology documentation",
                    "Stakeholder interview summaries",
                    "Evidence portfolio with sources",
                    "Problem analysis synthesis",
                    "Revised research questions"
                ],
                reflection_checkpoints=[
                    "What patterns emerge from our research?",
                    "Whose voices are we hearing? Whose are missing?",
                    "How has our understanding of the problem evolved?"
                ],
                duration_scaling_notes="Sprint: Secondary sources only. Unit: Add 2-3 stakeholder interviews. Journey: Comprehensive stakeholder engagement. Campaign: Longitudinal data collection."
            ),
            
            MilestoneTemplate(
                milestone_name="Solution Development & Testing",
                learning_purpose="Generate creative solutions and test feasibility through prototyping and feedback",
                core_activities=[
                    "Solution brainstorming and ideation",
                    "Feasibility analysis and criteria development",
                    "Prototype creation and testing",
                    "Stakeholder feedback collection",
                    "Solution refinement and iteration"
                ],
                essential_deliverables=[
                    "Multiple solution concepts",
                    "Feasibility analysis matrix",
                    "Solution prototypes or models",
                    "Stakeholder feedback documentation",
                    "Refined solution proposal"
                ],
                reflection_checkpoints=[
                    "Which solutions best address root causes?",
                    "What feedback challenged our assumptions?",
                    "How do we balance idealism with practicality?"
                ],
                duration_scaling_notes="Sprint: Single solution concept. Unit: 2-3 solution options with basic testing. Journey: Full prototype development. Campaign: Pilot implementation."
            ),
            
            MilestoneTemplate(
                milestone_name="Action Planning & Community Engagement",
                learning_purpose="Develop implementation strategy and engage authentic community audience",
                core_activities=[
                    "Implementation timeline development",
                    "Resource and partnership identification",
                    "Communication strategy design",
                    "Community presentation preparation",
                    "Action plan presentation and feedback"
                ],
                essential_deliverables=[
                    "Detailed action plan with timeline",
                    "Resource requirements and partnerships",
                    "Community presentation materials",
                    "Implementation next steps",
                    "Community feedback documentation"
                ],
                reflection_checkpoints=[
                    "Is our action plan realistic and achievable?",
                    "How did community members respond to our proposal?",
                    "What would we do differently in a real implementation?"
                ],
                duration_scaling_notes="Sprint: Basic action outline. Unit: Detailed plan with presentation. Journey: Community forum presentation. Campaign: Actual implementation launch."
            ),
            
            MilestoneTemplate(
                milestone_name="Reflection & Impact Assessment",
                learning_purpose="Synthesize learning, evaluate process, and consider broader implications",
                core_activities=[
                    "Learning synthesis and documentation",
                    "Process evaluation and improvement",
                    "Impact potential assessment",
                    "Civic engagement reflection",
                    "Next steps and commitment identification"
                ],
                essential_deliverables=[
                    "Individual learning portfolios",
                    "Team process evaluation",
                    "Impact assessment report",
                    "Civic engagement reflection essay",
                    "Future action commitments"
                ],
                reflection_checkpoints=[
                    "What did we learn about ourselves as civic actors?",
                    "How did this experience change our perspective?",
                    "What are our ongoing responsibilities to this issue?"
                ],
                duration_scaling_notes="All durations include this milestone - depth varies from simple reflection (Sprint) to comprehensive impact analysis (Campaign)."
            )
        ],
        
        assessment_framework=AssessmentFramework(
            formative_tools=[
                FormativeAssessmentTool(
                    tool_name="Research Learning Logs",
                    purpose="Document research process, sources, and evolving understanding",
                    implementation_guidance="Students maintain ongoing logs of research activities, key findings, and reflection questions",
                    frequency_recommendations={
                        Duration.SPRINT: "Daily entries",
                        Duration.UNIT: "After each research session",
                        Duration.JOURNEY: "Weekly comprehensive entries",
                        Duration.CAMPAIGN: "Bi-weekly with monthly synthesis"
                    },
                    scaling_guidance={
                        Duration.SPRINT: "Simple note-taking format",
                        Duration.UNIT: "Structured template with reflection prompts",
                        Duration.JOURNEY: "Comprehensive research portfolio",
                        Duration.CAMPAIGN: "Professional research documentation"
                    }
                ),
                FormativeAssessmentTool(
                    tool_name="Stakeholder Interview Reflections",
                    purpose="Process and synthesize stakeholder perspectives",
                    implementation_guidance="Structured reflection after each stakeholder interaction",
                    frequency_recommendations={
                        Duration.SPRINT: "Not applicable",
                        Duration.UNIT: "After each interview",
                        Duration.JOURNEY: "After each interview plus weekly synthesis",
                        Duration.CAMPAIGN: "After each interaction plus monthly analysis"
                    },
                    scaling_guidance={
                        Duration.SPRINT: "Focus on secondary sources",
                        Duration.UNIT: "Basic interview summaries",
                        Duration.JOURNEY: "Comprehensive stakeholder analysis",
                        Duration.CAMPAIGN: "Longitudinal relationship tracking"
                    }
                ),
                FormativeAssessmentTool(
                    tool_name="Solution Development Check-ins",
                    purpose="Monitor solution development process and thinking",
                    implementation_guidance="Regular check-ins during solution development with peer and teacher feedback",
                    frequency_recommendations={
                        Duration.SPRINT: "Mid-project check-in",
                        Duration.UNIT: "Weekly solution conferences",
                        Duration.JOURNEY: "Bi-weekly prototype reviews",
                        Duration.CAMPAIGN: "Monthly solution iterations"
                    },
                    scaling_guidance={
                        Duration.SPRINT: "Concept feedback only",
                        Duration.UNIT: "Prototype feedback and revision",
                        Duration.JOURNEY: "Comprehensive design thinking process",
                        Duration.CAMPAIGN: "Professional solution development cycle"
                    }
                )
            ],
            summative_moments=[
                SummativeAssessmentMoment(
                    moment_name="Community Problem Analysis",
                    purpose="Present research findings about the community problem and stakeholder perspectives",
                    typical_timing="After initial research phase",
                    assessment_focus=["Research quality", "Stakeholder analysis", "Problem definition"],
                    rubric_guidance="Assess depth of research, clarity of problem definition, and understanding of stakeholder perspectives"
                ),
                SummativeAssessmentMoment(
                    moment_name="Solution Prototype Demonstration",
                    purpose="Present and test potential solutions with peers and stakeholders",
                    typical_timing="Midway through solution development",
                    assessment_focus=["Creativity", "Feasibility", "Potential impact"],
                    rubric_guidance="Evaluate innovation, practicality, and potential community benefit of proposed solutions"
                ),
                SummativeAssessmentMoment(
                    moment_name="Community Action Plan Presentation",
                    purpose="Present final action plan to community stakeholders",
                    typical_timing="Final project presentation",
                    assessment_focus=["Clarity", "Feasibility", "Impact potential"],
                    rubric_guidance="Assess the completeness, practicality, and potential effectiveness of the proposed action plan"
                ),
                SummativeAssessmentMoment(
                    moment_name="Final Reflection Portfolio",
                    purpose="Document learning journey and personal growth",
                    typical_timing="Project conclusion",
                    assessment_focus=["Reflection depth", "Learning synthesis", "Future application"],
                    rubric_guidance="Evaluate depth of reflection, connection to learning goals, and plans for continued civic engagement"
                )
            ],
            reflection_protocols=[
                ReflectionProtocol(
                    protocol_name="Stakeholder Perspective Analysis",
                    purpose="Synthesize multiple stakeholder viewpoints on the community problem",
                    structure=[
                        "What did each stakeholder prioritize?",
                        "Where do stakeholder perspectives align or conflict?",
                        "What perspectives might we be missing?",
                        "How do power dynamics affect these perspectives?"
                    ],
                    timing_guidance="After completing stakeholder research phase",
                    facilitation_notes="Use graphic organizers to map stakeholder perspectives visually"
                ),
                ReflectionProtocol(
                    protocol_name="Civic Agency Development",
                    purpose="Reflect on growth as civic actors and community members",
                    structure=[
                        "How has my understanding of civic engagement changed?",
                        "What skills did I develop for community action?", 
                        "What responsibilities do I have to my community?",
                        "How will I continue to be civically engaged?"
                    ],
                    timing_guidance="Final project reflection",
                    facilitation_notes="Connect to broader civic education goals and ongoing opportunities"
                )
            ],
            portfolio_guidance="Students maintain comprehensive portfolios documenting research process, stakeholder engagement, solution development, and civic learning growth"
        ),
        
        authentic_audience_framework=AuthenticAudienceFramework(
            audience_categories=[
                "Community stakeholders directly affected by the problem",
                "Local government officials and policy makers",
                "Community organization leaders and activists",
                "Local business owners and employers",
                "Other community members and residents"
            ],
            engagement_formats=[
                "Community forum presentation and discussion",
                "Town hall or city council presentation",
                "Community organization partnership meeting",
                "Public showcase or exhibition",
                "Media presentation (local news, podcast, etc.)"
            ],
            preparation_requirements=[
                "Audience analysis and communication planning",
                "Professional presentation skill development",
                "Question and answer preparation",
                "Materials adaptation for non-academic audience",
                "Logistical coordination and scheduling"
            ],
            logistical_considerations=[
                "Venue accessibility and technology needs",
                "Appropriate timing for community member availability",
                "Cultural sensitivity and communication norms",
                "Follow-up and ongoing relationship building",
                "Documentation and permission considerations"
            ]
        ),
        
        project_management_tools=[
            "Team working agreements and role definitions",
            "Project timeline with milestone deadlines",
            "Research tracking and source management system",
            "Stakeholder contact and interview tracking",
            "Solution development and iteration log",
            "Community engagement planning calendar"
        ],
        
        recommended_resources=[
            "Local newspaper archives and online resources",
            "Community demographic and statistical data",
            "Government websites and public records",
            "Community organization contact directories",
            "Interview recording and transcription tools",
            "Presentation and portfolio creation platforms"
        ],
        
        technology_suggestions=[
            "Digital research and citation tools",
            "Interview recording apps or devices",
            "Collaborative document platforms",
            "Presentation software with multimedia capabilities",
            "Digital portfolio platforms",
            "Communication and scheduling tools"
        ],
        
        standards_alignment_examples={
            "social_studies": [
                "NCSS.D2.Civ.2.6-8: Analyze the role of citizens in the U.S. political system",
                "NCSS.D2.Civ.10.6-8: Explain the relevance of personal interests and perspectives to societal issues",
                "NCSS.D4.1.6-8: Construct arguments using claims and evidence from multiple sources"
            ],
            "english_language_arts": [
                "CCSS.ELA-LITERACY.WHST.6-8.1: Write arguments to support claims with clear reasons and relevant evidence",
                "CCSS.ELA-LITERACY.SL.7.4: Present claims and findings, emphasizing salient points",
                "CCSS.ELA-LITERACY.RST.6-8.7: Integrate quantitative or technical information expressed in words"
            ],
            "mathematics": [
                "CCSS.MATH.CONTENT.7.SP.B.3: Informally assess the degree of visual overlap of two numerical data distributions",
                "CCSS.MATH.CONTENT.8.SP.A.1: Construct and interpret scatter plots for bivariate measurement data"
            ],
            "cross_curricular": [
                "Critical thinking and problem solving",
                "Communication and collaboration", 
                "Research and inquiry skills",
                "Civic responsibility and engagement"
            ]
        },
        
        hqpbl_alignment=HQPBLAlignment(
            intellectual_challenge="Students engage in complex problem analysis, stakeholder perspective synthesis, and solution design requiring higher-order thinking skills",
            authenticity="Real community problems with genuine stakeholder engagement and potential for actual impact",
            public_product="Community presentations to authentic audiences including affected stakeholders and decision-makers",
            collaboration="Team-based research and solution development with distributed roles and shared accountability",
            project_management="Multi-phase timeline with milestone deliverables, stakeholder coordination, and resource management",
            reflection="Ongoing reflection on research process, stakeholder perspectives, civic engagement, and personal growth as community members"
        ),
        
        compatibility_matrix=CompatibilityMatrix(
            duration_compatible=[Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN],
            social_structure_compatible=[SocialStructure.COLLABORATIVE, SocialStructure.COMMUNITY_CONNECTED, SocialStructure.NETWORKED],
            cognitive_complexity_range=[CognitiveComplexity.ANALYSIS, CognitiveComplexity.SYNTHESIS, CognitiveComplexity.EVALUATION],
            authenticity_compatible=[AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED, AuthenticityLevel.IMPACT],
            scaffolding_compatible=[ScaffoldingIntensity.FACILITATED, ScaffoldingIntensity.INDEPENDENT, ScaffoldingIntensity.MENTORED],
            product_complexity_compatible=[ProductComplexity.PORTFOLIO, ProductComplexity.SYSTEM, ProductComplexity.EXPERIENCE],
            delivery_mode_compatible=[DeliveryMode.FACE_TO_FACE, DeliveryMode.HYBRID, DeliveryMode.SYNCHRONOUS_REMOTE]
        ),
        
        teacher_preparation_notes=[
            "Establish relationships with community stakeholders before project launch",
            "Research local community issues and identify authentic problems suitable for student investigation",
            "Prepare interview question stems and research methodology resources",
            "Plan logistics for community presentations including venue, technology, and audience coordination",
            "Develop rubrics aligned with both academic standards and civic engagement outcomes",
            "Consider safety and permission requirements for community engagement activities"
        ],
        
        common_challenges=[
            "Balancing academic rigor with authentic community engagement",
            "Managing diverse stakeholder perspectives and potential conflicts",
            "Coordinating schedules with community members for interviews and presentations",
            "Helping students navigate complex social and political issues appropriately",
            "Ensuring all students can participate meaningfully regardless of community connections",
            "Managing scope to prevent projects from becoming overwhelming"
        ],
        
        success_indicators=[
            "Students demonstrate genuine investment in their chosen community problem",
            "Research shows evidence of multiple stakeholder perspectives and credible sources",
            "Solutions are grounded in evidence and show consideration of feasibility",
            "Community presentations engage authentic audiences in meaningful dialogue",
            "Students can articulate their growth as civic actors and community members",
            "Projects result in continued student engagement with community issues"
        ],

        # Progressive Education Integration (NEW)
        inquiry_framework=InquiryFramework(
            what_we_know_prompts=[
                "What do we already know about problems in our community?",
                "What have we heard adults talking about regarding local issues?",
                "What do we notice when we walk around our neighborhood?",
                "What community challenges affect our families directly?"
            ],
            what_we_wonder_prompts=[
                "What makes some community problems harder to solve than others?",
                "Why do different people see the same problem differently?",
                "What would happen if we could fix this problem?",
                "Who has the power to make changes in our community?"
            ],
            what_we_want_to_learn_prompts=[
                "How can we understand all sides of this community issue?",
                "What would real community members want us to know?",
                "How do successful community changes actually happen?",
                "What role can young people play in community problem-solving?"
            ],
            how_we_might_explore_options=[
                "Interview community members with different perspectives",
                "Research similar problems in other communities",
                "Shadow local officials or activists for a day",
                "Create surveys to gather community input",
                "Attend community meetings as observers"
            ],
            reflection_return_prompts=[
                "How has our understanding of this problem grown deeper?",
                "What surprised us most about community perspectives?",
                "How do we see our role in the community differently now?",
                "What new questions emerged that we didn't expect?"
            ]
        ),

        learning_environment_framework=LearningEnvironmentFramework(
            physical_space_invitations=[
                "Community issues bulletin board with rotating local news",
                "Stakeholder perspective mapping wall with photos and quotes",
                "Solutions brainstorming corner with sticky notes and markers",
                "Interview practice space with recording equipment setup",
                "Action planning table with timelines and resource lists"
            ],
            documentation_displays=[
                "Learning journey timeline showing how understanding evolved",
                "Quote collection from community interviews",
                "Photo documentation of research process and community visits",
                "Solution prototype gallery with iteration notes",
                "Reflection wall showing growth in civic thinking"
            ],
            material_provocations=[
                "Local newspaper clippings highlighting community challenges",
                "Demographic data visualizations about the local area",
                "Photos of community spaces showing both assets and needs",
                "Artifacts from successful community change efforts",
                "Tools and materials for creating solution prototypes"
            ],
            collaboration_zones=[
                "Research team stations for deep investigation work",
                "Interview preparation circles for practice and feedback",
                "Solution development labs for creative problem-solving",
                "Presentation rehearsal space for community audience prep",
                "Reflection retreat corner for individual processing"
            ],
            reflection_retreats=[
                "Quiet journaling nook for individual reflection",
                "Comfortable reading area with community problem resources",
                "Meditation/thinking space for processing complex issues",
                "Individual conference corner for teacher check-ins"
            ]
        ),

        student_agency_framework=StudentAgencyFramework(
            natural_choice_points=[
                "Select which community problem speaks to your team's passions",
                "Choose research methods that match your strengths and interests",
                "Decide which stakeholders you want to interview",
                "Pick the format for presenting solutions to the community",
                "Choose how to document and share your learning journey"
            ],
            voice_amplification_strategies=[
                "Each team member leads research on one stakeholder perspective",
                "Students facilitate community forums rather than just presenting",
                "Peer teaching sessions where teams share research findings",
                "Student-created interview questions drive stakeholder conversations",
                "Youth perspectives are highlighted as unique and valuable"
            ],
            ownership_transfer_milestones=[
                "Students generate and revise their own research questions",
                "Teams self-manage interview scheduling and logistics",
                "Students adapt project timeline based on community feedback",
                "Teams decide on solution testing methods and criteria",
                "Students plan and facilitate their own community presentations"
            ],
            peer_collaboration_structures=[
                "Research buddy system for interview preparation and debrief",
                "Cross-team solution critique sessions for feedback",
                "Peer mentoring for presentation and communication skills",
                "Collaborative problem-solving when facing research obstacles",
                "Team-to-team sharing of successful community connections"
            ]
        ),

        documentation_framework=DocumentationFramework(
            learning_capture_opportunities=[
                "Photo-document initial reactions to community problems",
                "Record 'aha moments' during stakeholder interviews",
                "Capture solution brainstorming and iteration processes",
                "Document community presentation preparation and delivery",
                "Video reflection conversations about civic growth"
            ],
            student_thinking_artifacts=[
                "Stakeholder perspective maps showing evolving understanding",
                "Research question evolution showing deepening inquiry",
                "Solution prototype sketches and iteration notes",
                "Community feedback integration and response documentation",
                "Personal civic identity reflection essays and visuals"
            ],
            process_documentation_methods=[
                "Learning timeline with photos, quotes, and reflection notes",
                "Research journey portfolio with sources, findings, and questions",
                "Solution development log showing testing and refinement",
                "Community engagement documentation with feedback integration",
                "Civic learning growth portfolio with before/after perspectives"
            ],
            celebration_sharing_formats=[
                "Community showcase with interactive problem-solution displays",
                "Local media features highlighting student civic engagement",
                "School-wide presentation inspiring other classes to take action",
                "Community forum where students facilitate ongoing dialogue",
                "Digital storytelling sharing the learning journey with families"
            ]
        ),

        expression_pathways=ExpressionPathways(
            visual_expression_options=[
                "Infographic timelines showing problem development over time",
                "Stakeholder perspective maps with photos and quotes",
                "Solution prototype sketches and visual mockups",
                "Data visualization showing community problem statistics",
                "Photo essays documenting the research and engagement journey"
            ],
            kinesthetic_expression_options=[
                "Role-playing different stakeholder perspectives in community forums",
                "Building physical models or prototypes of proposed solutions",
                "Community walking tours to demonstrate problems and solutions",
                "Interactive demonstrations of how solutions would work",
                "Service learning activities implementing aspects of solutions"
            ],
            verbal_expression_options=[
                "Stakeholder interview podcasts sharing community voices",
                "Community forum facilitation and dialogue leadership",
                "Storytelling sessions sharing research findings narratively",
                "Debate formats exploring different solution approaches",
                "Town hall presentations with Q&A engagement"
            ],
            collaborative_expression_options=[
                "Multi-team community problem solution expo",
                "Cross-generational dialogue sessions with community members",
                "Collaborative murals depicting community challenges and assets",
                "Group-facilitated community input sessions",
                "Peer teaching workshops sharing research methodologies"
            ],
            creative_expression_options=[
                "Documentary films following the research and solution process",
                "Community problem theater performances exploring different perspectives",
                "Musical compositions inspired by community stories and data",
                "Creative writing pieces from multiple stakeholder viewpoints",
                "Art installations highlighting community assets and challenges"
            ]
        ),

        emergent_learning_support=EmergentLearningSupport(
            pivot_opportunity_indicators=[
                "When students discover unexpected connections between problems",
                "When community interviews reveal different issues than anticipated",
                "When solution testing uncovers more fundamental problems",
                "When students express passion for related but different community issues",
                "When community feedback suggests new directions for investigation"
            ],
            student_interest_amplifiers=[
                "Create individual research tracks within team problem focus",
                "Allow students to pursue personal connections to community issues",
                "Support student-initiated additional stakeholder interviews",
                "Encourage exploration of problems students have experienced directly",
                "Provide time for individual passion project threads within team work"
            ],
            unexpected_connection_bridges=[
                "Help students see links between different community problems",
                "Connect local issues to broader social justice themes students care about",
                "Bridge community problems to students' academic interests and strengths",
                "Link current community issues to historical patterns students discover",
                "Connect individual family experiences to broader community challenges"
            ],
            community_opportunity_integrators=[
                "Invite additional community members when students express curiosity",
                "Arrange field experiences when students want deeper understanding",
                "Connect students with ongoing community initiatives they can join",
                "Facilitate student attendance at relevant community meetings",
                "Support student creation of ongoing community engagement opportunities"
            ]
        ),
        
        # Teacher Support
        getting_started_essentials=[
            "Identify 2-3 local community issues that students might connect with",
            "Reach out to 1-2 community partners who could provide authentic context",
            "Create a simple stakeholder interview template for student research",
            "Set up a physical or digital space for documenting the learning journey",
            "Plan an initial community walk or observation experience to spark curiosity"
        ],
        when_things_go_wrong=[
            "If students struggle to identify problems: Bring in guest speakers from community organizations",
            "If research stalls: Provide structured interview guides and practice sessions",
            "If solutions seem unrealistic: Connect with mentors who can provide feedback",
            "If community partners are unavailable: Use case studies and simulations temporarily",
            "If team conflicts arise: Implement structured protocols for respectful disagreement"
        ],
        signs_of_success=[
            "Students initiate conversations about community issues outside of class time",
            "Research extends beyond minimum requirements to seek deeper understanding",
            "Solutions evolve through multiple iterations based on feedback",
            "Students make authentic connections with community stakeholders",
            "Project work leads to actual community impact or continued engagement"
        ],
        
        # Additional Teacher Decision-Making Support
        teacher_prep_essentials=[
            "Identify 2-3 local community contacts willing to be interviewed",
            "Research current community issues through local news/data",
            "Plan logistics for potential community presentation venue"
        ],
        student_readiness="Works best with students who can conduct respectful interviews and handle complex social issues. Adaptable for all grade levels with appropriate scaffolding.",
        community_engagement_level="Moderate - requires 2-3 community stakeholder interviews and one authentic audience presentation",
        assessment_highlights=[
            "Students document their learning journey through research portfolios",
            "Community members provide authentic feedback on student solutions", 
            "Final presentations are delivered to real audiences who can take action"
        ],
        assessment_focus="Process growth, community impact potential, civic identity development",
        what_success_looks_like="Students become genuinely invested in their community issue, develop relationships with local stakeholders, and present actionable solutions that community members take seriously. Many students continue civic engagement beyond the project.",
        
        # Key Elements for Teacher Overview
        final_product_description="Community Action Plan with implementation strategy and stakeholder presentation",
        core_skills=[
            BaseTemplate.CoreSkill(
                skill_name="Research & Data Analysis",
                application="Students collect and analyze community data to identify problems and evaluate solutions",
                assessment_connection="Evaluated through research quality and evidence-based conclusions"
            ),
            BaseTemplate.CoreSkill(
                skill_name="Systems Thinking",
                application="Students map community systems and identify intervention points for change",
                assessment_connection="Evaluated through stakeholder analysis and solution viability"
            ),
            BaseTemplate.CoreSkill(
                skill_name="Communication & Advocacy",
                application="Students develop persuasive presentations for authentic community audiences",
                assessment_connection="Evaluated through final presentation and stakeholder feedback"
            )
        ]
    )