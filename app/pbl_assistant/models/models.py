from pydantic import BaseModel
from typing import List, Optional, Dict, Union
from enum import Enum

class GradeLevel(str, Enum):
    K = "K"
    GRADE_1 = "1"
    GRADE_2 = "2"
    GRADE_3 = "3"
    GRADE_4 = "4"
    GRADE_5 = "5"
    GRADE_6 = "6"
    GRADE_7 = "7"
    GRADE_8 = "8"
    GRADE_9 = "9"
    GRADE_10 = "10"
    GRADE_11 = "11"
    GRADE_12 = "12"

class SubjectArea(str, Enum):
    SCIENCE = "Science"
    MATHEMATICS = "Mathematics"
    ELA = "English Language Arts"
    SOCIAL_STUDIES = "Social Studies"
    ARTS = "Arts"
    TECHNOLOGY = "Technology"
    ENGINEERING = "Engineering"
    HEALTH = "Health"
    PHYSICAL_EDUCATION = "Physical Education"


# Project Profiling - First Agent Stage
class ProjectIntent(str, Enum):
    SCIENTIFIC_INQUIRY = "Scientific Inquiry"           # Hypothesis-driven investigation
    ENGINEERING_DESIGN = "Engineering Design"          # Problem-solving with constraints
    CREATIVE_EXPRESSION = "Creative Expression"        # Arts-integrated projects
    RESEARCH_INVESTIGATION = "Research Investigation"   # Information gathering and analysis
    COMMUNITY_ACTION = "Community Action"               # Real-world problem solving
    SKILL_APPLICATION = "Skill Application"            # Practice and mastery focus
    INTERDISCIPLINARY = "Interdisciplinary"            # Multiple subjects integrated
    TECHNOLOGY_FOCUSED = "Technology Focused"          # Digital creation/coding
    HISTORICAL_INQUIRY = "Historical Inquiry"          # Past events investigation
    MATHEMATICAL_MODELING = "Mathematical Modeling"     # Math concepts through real scenarios

class ContentArea(str, Enum):
    STEM_HEAVY = "STEM Heavy"                          # Science, Math, Engineering dominant
    HUMANITIES_FOCUSED = "Humanities Focused"         # ELA, Social Studies, Arts
    BALANCED_INTEGRATION = "Balanced Integration"      # Equal subject representation
    CAREER_TECHNICAL = "Career/Technical"              # Vocational skills focus
    LIFE_SKILLS = "Life Skills"                       # Health, citizenship, practical skills


class TeacherRequest(BaseModel):
    raw_message: str

class ProjectDetails(BaseModel):
    """First-stage agent analysis of teacher request"""
    topic: str = Field(..., description="The main topic or subject of the project")
    grade_level: Union[GradeLevel, str] = Field(..., description="Grade level of students")
    duration_preference: str = Field(..., description="Preferred duration of the project")
    age_range: Optional[Dict[str, int]] = Field(
        None,
        description="Age range of students (min/max)"
    )
    primary_intent: ProjectIntent = Field(..., description="Primary goal or purpose of the project")
    secondary_intents: List[ProjectIntent] = Field(
        default_factory=list,
        description="Additional goals or purposes of the project"
    )
    content_area_focus: ContentArea = Field(..., description="Primary subject area focus")
    learning_outcomes: List[str] = Field(
        default_factory=list,
        description="List of intended learning outcomes"
    )
    
    # Project characteristics
    requires_experimentation: bool = Field(
        False,
        description="Whether the project involves lab work or testing"
    )
    involves_data_collection: bool = Field(
        False,
        description="Whether the project includes surveys, measurements, or observations"
    )
    needs_mathematical_analysis: bool = Field(
        False,
        description="Whether the project requires calculations, graphing, or statistics"
    )
    includes_design_challenge: bool = Field(
        False,
        description="Whether the project involves building, creating, or prototyping"
    )
    uses_technology_tools: bool = Field(
        False,
        description="Whether the project uses software, apps, or digital creation tools"
    )
    community_connection_desired: bool = Field(
        False,
        description="Whether the project has a real-world audience or local relevance"
    )
    hands_on_emphasis: bool = Field(
        False,
        description="Whether the project emphasizes maker activities or manipulatives"
    )
    research_intensive: bool = Field(
        False,
        description="Whether the project focuses on reading, investigating, or citing sources"
    )
    presentation_focused: bool = Field(
        False,
        description="Whether the project emphasizes communication or public speaking"
    )
    collaborative_emphasis: bool = Field(
        False,
        description="Whether the project requires group work"
    )
    
    # Resource and constraint indicators
    materials_mentioned: bool = Field(
        False,
        description="Whether specific materials were mentioned in the request"
    )
    resource_limitations_mentioned: bool = Field(
        False,
        description="Whether resource constraints were mentioned"
    )
    time_constraints_noted: bool = Field(
        False,
        description="Whether time limitations were mentioned"
    )
    
    # Additional project details
    assessment_requirements: Optional[List[str]] = Field(
        default_factory=list,
        description="Specific assessment methods or requirements"
    )
    cultural_considerations: Optional[List[str]] = Field(
        default_factory=list,
        description="Cultural aspects to consider in the project"
    )
    implicit_goals: Optional[List[str]] = Field(
        default_factory=list,
        description="Unofficial or unstated goals of the project"
    )
    class_interests: Optional[List[str]] = Field(
        default_factory=list,
        description="Specific interests of the class or students"
    )
    standard_codes: List[str] = Field(
        default_factory=list,
        description="List of educational standard codes the project addresses"
    )
    real_world_exploration: bool = Field(
        False,
        description="Whether the project involves real-world exploration or application"
    )
    places_to_visit: Optional[List[str]] = Field(
        default_factory=list,
        description="Potential field trip locations or places to visit"
    )
    skills_to_develop: Optional[List[str]] = Field(
        default_factory=list,
        description="Specific skills students should develop through the project"
    )
    end_product: Optional[str] = Field(
        "",
        description="The final product or deliverable of the project"
    )
    
# Class Profile Models
class SchoolType(str, Enum):
    PUBLIC_TRADITIONAL = "Public Traditional"
    PUBLIC_CHARTER = "Public Charter"
    PRIVATE_SECULAR = "Private Secular"
    PRIVATE_RELIGIOUS = "Private Religious"
    INTERNATIONAL = "International"
    HOMESCHOOL_COOP = "Homeschool Cooperative"
    ALTERNATIVE = "Alternative School"
    VOCATIONAL = "Vocational/Technical"
    SPECIAL_NEEDS = "Special Needs"
    INDIGENOUS_COMMUNITY = "Indigenous Community School"
    RURAL_MULTIGRADE = "Rural Multigrade"

class ClassroomSetting(str, Enum):
    TRADITIONAL = "Traditional Classroom"
    FLEXIBLE_SEATING = "Flexible Seating"
    OUTDOOR = "Outdoor Classroom"
    MULTI_PURPOSE = "Multi-purpose Room"
    LABORATORY = "Laboratory/Maker Space"
    LIBRARY = "Library/Media Center"
    MOBILE = "Mobile/Traveling Classroom"
    HOME = "Home Environment"
    COMMUNITY_CENTER = "Community Center"

class LanguageProfile(BaseModel):
    primary_language: str
    english_proficiency_levels: Dict[str, int] = {}  # student_id -> proficiency level 1-5
    multilingual_students: int = 0
    heritage_languages: List[str] = []
    translation_needs: bool = False

class SpecialNeeds(BaseModel):
    iep_students: int = 0  # Individualized Education Program
    section_504_students: int = 0  # Section 504 accommodations
    gifted_talented: int = 0
    learning_disabilities: List[str] = []
    physical_accommodations: List[str] = []
    behavioral_supports: List[str] = []
    assistive_technologies: List[str] = []

class AcademicProfile(BaseModel):
    # Performance Data
    grade_level_performance: Dict[str, str] = {}  # subject -> "below", "at", "above"
    standardized_test_scores: Dict[str, float] = {}
    literacy_levels: Dict[str, int] = {}  # reading level distribution *Blast*
    math_skill_gaps: List[str] = []
    # Prior Experience
    pbl_experience: str = "none"  # "none", "some", "extensive"
    technology_comfort: str = "low"  # "low", "medium", "high"
    collaborative_work_experience: str = "limited"

class CulturalContext(BaseModel):
    # Demographics
    ethnic_composition: Dict[str, int] = {}  # ethnicity -> count
    
    # Community Context
    rural_urban_suburban: str = "suburban"
    community_challenges: List[str] = []
    community_assets: List[str] = []
    local_knowledge_systems: List[str] = []
    
    # Family Engagement
    transportation_barriers: bool = False
    language_barriers: bool = False
    technology_access_at_home: str = "limited"

class ResourceInventory(BaseModel):
    # Technology
    computers: int = 0
    tablets: int = 0
    interactive_whiteboard: bool = False
    projector: bool = False
    internet_quality: str = "none"  # "none", "poor", "adequate", "excellent"
    
    # Materials
    textbooks_per_student: float = 0.0
    library_books: int = 0
    science_equipment: List[str] = []
    art_supplies: List[str] = []
    sports_equipment: List[str] = []
    manipulatives: List[str] = []
    
    # Infrastructure
    electricity_reliable: bool = True
    heating_cooling: str = "none"  # "none", "basic", "climate_controlled"
    natural_light: str = "poor"    # "poor", "adequate", "excellent"
    outdoor_space: bool = False
    
    # Community Resources
    public_library_access: bool = False
    museum_access: bool = False
    community_experts: List[str] = []
    field_trip_possibilities: List[str] = []
    parent_volunteer_availability: str = "low"  # "low", "medium", "high"

class TeacherProfile(BaseModel):
    experience_years: int
    pbl_training: str = "none"  # "none", "workshop", "certification", "expert"
    subject_expertise: List[str] = []
    technology_comfort: str = "basic"  # "basic", "intermediate", "advanced"
    collaboration_time: str = "limited"  # "none", "limited", "adequate", "extensive"
    planning_time: str = "limited"
    professional_development_access: str = "limited"
    administrative_support: str = "adequate"

class ClassProfile(BaseModel):
    # Basic Demographics
    total_students: int
    grade_level: Union[GradeLevel, str, List[str]]  # Can be mixed grades
    age_range: Dict[str, int]  # "min_age", "max_age", "average_age"
    gender_distribution: Dict[str, int] | None = None
    
    # Institutional Context
    school_type: SchoolType
    classroom_setting: ClassroomSetting
    class_size_category: str = "medium"  # "small" (<15), "medium" (15-25), "large" (>25)
    
    # Learning Context
    language_profile: LanguageProfile
    special_needs: SpecialNeeds
    academic_profile: AcademicProfile | None = None
    cultural_context: CulturalContext | None = None
    
    # Resources and Constraints
    resource_inventory: ResourceInventory | None = None
    teacher_profile: TeacherProfile | None = None
    
    # Schedule and Time
    class_period_length: int | None = None
    periods_per_week: int | None = None
    flexible_scheduling: bool | None = None
    block_scheduling: bool | None = None
    
    # Challenges and Opportunities
    primary_challenges: List[str] | None = None
    unique_opportunities: List[str] | None = None
    community_partnerships_available: List[str] | None = None
    
    # PBL Readiness
    collaboration_readiness: str | None = None
    technology_integration_readiness: str | None = None
    family_engagement_potential: str | None = None
    real_world_connection_opportunities: List[str] | None = None

# Helper model for agent decision-making
class ClassProfileSummary(BaseModel):
    """Condensed profile for quick agent decision-making"""
    key_constraints: List[str]  # Most limiting factors
    key_opportunities: List[str]  # Biggest advantages
    adaptation_priorities: List[str]  # What needs most accommodation
    strength_areas: List[str]  # What to build upon
    recommended_pbl_complexity: str = "moderate"  # "simple", "moderate", "complex"
    suggested_project_duration: str = "2-3 weeks"
    technology_integration_level: str = "basic"
    community_engagement_feasibility: str = "moderate"
    
#Testing
class LearningStrategies(BaseModel):
    research_basis: List[str]  # Citations/theories
    pedagogical_strategies: List[str]
    engagement_tactics: List[str]
    differentiation_approaches: List[str]
    motivation_techniques: List[str]

class ScaffoldingPlan(BaseModel):
    prerequisite_skills: List[str]
    scaffolding_sequence: List[str]
    support_structures: List[str]
    gradual_release_plan: List[str]
    assessment_checkpoints: List[str]
    

class ActivityLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

class AssessmentType(str, Enum):
    FORMATIVE = "Formative"
    SUMMATIVE = "Summative"
    PEER = "Peer"
    SELF = "Self"

class ProductType(str, Enum):
    INDIVIDUAL = "Individual"
    TEAM = "Team"
    PUBLIC = "Public"

class UDLNetwork(str, Enum):
    RECOGNITION = "Recognition"  # Multiple means of representation
    STRATEGIC = "Strategic"      # Multiple means of engagement
    AFFECTIVE = "Affective"      # Multiple means of action/expression

class DepthOfKnowledge(int, Enum):
    RECALL = 1
    SKILL_CONCEPT = 2
    STRATEGIC_THINKING = 3
    EXTENDED_THINKING = 4

class BloomLevel(str, Enum):
    REMEMBER = "Remember"
    UNDERSTAND = "Understand"
    APPLY = "Apply"
    ANALYZE = "Analyze"
    EVALUATE = "Evaluate"
    CREATE = "Create" 

class BloomAction(BaseModel):
    level: BloomLevel
    action_verbs: List[str]
    sample_prompts: List[str]
    assessment_strategies: List[str]

class BloomsTaxonomy(BaseModel):
    remember: BloomAction = BloomAction(
        level=BloomLevel.REMEMBER,
        action_verbs=["define", "list", "recall", "identify", "name", "state", "describe", "match", "select", "label"],
        sample_prompts=["List the main components of...", "Define the term...", "What are the facts about..."],
        assessment_strategies=["multiple_choice", "fill_in_blank", "matching", "true_false", "short_answer"]
    )
    understand: BloomAction = BloomAction(
        level=BloomLevel.UNDERSTAND,
        action_verbs=["explain", "summarize", "paraphrase", "interpret", "classify", "compare", "contrast", "demonstrate"],
        sample_prompts=["Explain in your own words...", "What is the main idea of...", "How would you summarize..."],
        assessment_strategies=["concept_maps", "graphic_organizers", "explanation", "demonstration", "examples"]
    )
    apply: BloomAction = BloomAction(
        level=BloomLevel.APPLY,
        action_verbs=["use", "apply", "implement", "solve", "demonstrate", "operate", "construct", "calculate"],
        sample_prompts=["How would you use this to solve...", "Apply this concept to...", "Calculate the result when..."],
        assessment_strategies=["problem_solving", "case_studies", "simulations", "demonstrations", "projects"]
    )
    analyze: BloomAction = BloomAction(
        level=BloomLevel.ANALYZE,
        action_verbs=["analyze", "examine", "compare", "contrast", "categorize", "differentiate", "investigate", "question"],
        sample_prompts=["What are the parts of...", "How do these relate to...", "What patterns do you see..."],
        assessment_strategies=["data_analysis", "case_studies", "debates", "research", "graphic_organizers"]
    )
    evaluate: BloomAction = BloomAction(
        level=BloomLevel.EVALUATE,
        action_verbs=["evaluate", "judge", "critique", "assess", "justify", "argue", "defend", "support", "prioritize"],
        sample_prompts=["What is your opinion on...", "Judge the value of...", "What criteria would you use to assess..."],
        assessment_strategies=["rubrics", "peer_review", "self_assessment", "debates", "critiques"]
    )
    create: BloomAction = BloomAction(
        level=BloomLevel.CREATE,
        action_verbs=["create", "design", "develop", "compose", "construct", "plan", "produce", "invent", "generate"],
        sample_prompts=["Design a solution for...", "Create a new approach to...", "Develop a plan to..."],
        assessment_strategies=["projects", "portfolios", "presentations", "original_works", "innovations"]
    )

class LearningObjectiveBloom(BaseModel):
    objective: str
    bloom_level: BloomLevel
    action_verb: str
    assessment_alignment: str
    complexity_level: int  # 1-5 scale within the Bloom level

class CollaborationRole(str, Enum):
    FACILITATOR = "Facilitator"
    RESEARCHER = "Researcher"
    RECORDER = "Recorder"
    TIMEKEEPER = "Timekeeper"
    MATERIALS_MANAGER = "Materials Manager"
    PRESENTER = "Presenter"
    QUALITY_CHECKER = "Quality Checker"

# Enhanced learning progression models
class LearningProgression(BaseModel):
    prerequisite_skills: List[str]
    target_understanding: str
    intermediate_benchmarks: List[str]
    common_misconceptions: List[str]
    assessment_checkpoints: List[str]

class TransferScaffold(BaseModel):
    near_transfer_opportunities: List[str]  # Similar contexts
    far_transfer_opportunities: List[str]   # Different contexts
    bridging_questions: List[str]           # Help students see connections
    application_contexts: List[str]         # Real-world applications

# Enhanced UDL integration
class UDLSupport(BaseModel):
    network: UDLNetwork
    strategies: List[str]
    tools: List[str]
    success_indicators: List[str]

class MultimodalRepresentation(BaseModel):
    visual: List[str] = []        # Charts, diagrams, videos
    auditory: List[str] = []      # Podcasts, discussions, music
    kinesthetic: List[str] = []   # Hands-on activities, movement
    digital: List[str] = []       # Interactive media, simulations

# Structured reflection and metacognition
class ReflectionScaffold(BaseModel):
    timing: str  # "daily", "phase_end", "project_end"
    prompts: List[str]
    tools: List[str]  # "journal", "peer_conference", "video_log"
    success_criteria_focus: List[str]
    metacognitive_strategies: List[str]

# Enhanced collaboration structures
class CollaborationStructure(BaseModel):
    group_formation_strategy: str
    roles: List[CollaborationRole]
    role_rotation_schedule: str
    interdependence_mechanisms: List[str]  # How students depend on each other
    individual_accountability: List[str]    # How individual learning is ensured
    social_skills_focus: List[str]         # Communication, conflict resolution, etc.
    team_building_activities: List[str]

class StudentChoice(BaseModel):
    choice_points: List[str]  # Where students make decisions
    option_types: List[str]   # "product_format", "research_path", "presentation_style"
    scaffolds_for_choice: List[str]  # How to support decision-making
    autonomy_supports: List[str]     # Structures that promote independence

# Enhanced design thinking integration
class DesignThinkingScaffold(BaseModel):
    phase: str  # "empathize", "define", "ideate", "prototype", "test"
    guiding_questions: List[str]
    tools_and_protocols: List[str]
    success_criteria: List[str]
    time_allocation: str
    materials_needed: List[str]

# Enhanced standards model
class Standard(BaseModel):
    subject: str
    code: str
    description: str
    grade_level: Optional[str] = None
    performance_indicators: List[str]
    depth_of_knowledge_level: DepthOfKnowledge
    cross_curricular_connections: List[str]
    learning_progression: Optional[LearningProgression] = None

class LearningGoal(BaseModel):
    category: str  # "content_knowledge" or "success_skills"
    skill_area: str  # e.g., "creativity", "critical_thinking", "collaboration"
    description: str
    success_criteria: List[str]
    learning_progression: LearningProgression
    transfer_goals: TransferScaffold
    core_skills_addressed: List[CoreSkill] = []  # NEW
    skill_integration_strategy: str = ""         # NEW - how skills connect
    cross_skill_connections: List[str] = []      # NEW - how skills reinforce each other

#Skills
class CoreSkillArea(str, Enum):
    ELA = "English Language Arts"
    MATHEMATICS = "Mathematics" 
    TECHNOLOGY_LITERACY = "Technology Literacy"
    ENGINEERING_DESIGN = "Engineering Design"
    SCIENTIFIC_THINKING = "Scientific Thinking"

class CoreSkill(BaseModel):
    skill_area: CoreSkillArea
    standard_code: str  # CCSS.ELA-LITERACY.RST.9-10.7 or NGSS.K-2-ETS1-1
    skill_description: str
    performance_expectations: List[str]
    assessment_methods: List[str]
    integration_level: str  # "primary", "secondary", "supporting"

class SkillIntegrationStrategy(BaseModel):
    skill_combination: List[CoreSkillArea]  # Which skills work together
    integration_approach: str               # "authentic", "explicit", "reinforcing"
    real_world_application: str             # How this combo appears in real work
    assessment_approach: str                # How to assess the integrated skills

class CoreSkillsFramework(BaseModel):
    project_skill_priorities: List[CoreSkill]           # Most important for this project
    skill_integration_strategies: List[SkillIntegrationStrategy]
    skill_progression_map: Dict[str, List[str]]         # phase -> skills developed
    cross_curricular_connections: List[str]             # How skills reinforce each other

class STEAMFocus(BaseModel):
    science: List[str] = []
    technology: List[str] = []
    engineering: List[str] = []
    arts: List[str] = []
    mathematics: List[str] = []
    integration_strategies: List[str] = []  # How subjects connect

# Technology integration with TPACK
class TechnologyIntegration(BaseModel):
    tool_name: str
    pedagogical_purpose: str      # How it supports learning
    content_connection: str       # How it connects to subject matter
    technical_skills_required: List[str]
    learning_enhancement: str     # How it improves the learning experience

# Enhanced learning experience model
class LearningExperience(BaseModel):
    name: str
    description: str
    duration: str
    learning_objectives: List[str]
    prerequisite_check: Optional[str]
    steam_integration: List[str]
    technology_integration: List[TechnologyIntegration] = []
    cultural_connection: Optional[str] = None
    design_thinking_scaffolds: List[DesignThinkingScaffold] = []
    success_criteria: List[str]
    formative_checkpoints: List[str]
    multimodal_representations: MultimodalRepresentation
    udl_supports: List[UDLSupport] = []
    student_choice: Optional[StudentChoice] = None
    collaboration_structure: Optional[CollaborationStructure] = None
    primary_core_skills: List[CoreSkill] = []         # NEW - main focus
    secondary_core_skills: List[CoreSkill] = []       # NEW - reinforced skills
    skill_scaffolding: Dict[str, List[str]] = {}      # NEW - skill_area -> scaffolds
    skill_success_criteria: Dict[str, List[str]] = {} # NEW - skill_area -> criteria

class ProjectPhase(BaseModel):
    phase_number: int
    title: str
    duration: str
    milestone: str
    key_question: str
    learning_experiences: List[LearningExperience]
    scaffolds: List[str] = []
    anticipated_questions: List[str] = []
    reflection_scaffolds: List[ReflectionScaffold] = []
    formative_assessments: List[str] = []  # Frequent check-ins
    core_skills_focus: List[CoreSkill] = []              # NEW
    skill_building_activities: List[str] = []            # NEW
    skill_assessment_checkpoints: List[str] = []         # NEW
    skill_progression_evidence: List[str] = []           # NEW

class Product(BaseModel):
    name: str
    description: str
    type: ProductType
    format: Optional[str] = None
    choice_options: List[str] = []  # Different ways students can create product
    success_criteria: List[str] = []
    transfer_connections: List[str] = []  # How this connects to real world

# Enhanced assessment with frequent feedback loops
class Assessment(BaseModel):
    name: str
    type: AssessmentType
    format: str
    purpose: Optional[str] = None
    timing: str
    feedback_mechanisms: List[str]  # How students receive feedback
    learning_progression_alignment: Optional[str] = None
    transfer_focus: List[str] = []  # What transfers this assesses
    core_skills_assessed: List[SkillAssessment] = []  # NEW
    skill_transfer_evidence: List[str] = []           # NEW

class SkillAssessment(BaseModel):
    core_skill: CoreSkill
    assessment_type: str  # "performance_task", "portfolio", "demonstration", "test"
    timing: str          # "ongoing", "phase_end", "project_end"
    success_criteria: List[str]
    evidence_collection: List[str]  # What artifacts demonstrate mastery
    rubric_focus: List[str]         # Specific rubric elements

class Resource(BaseModel):
    name: str
    type: str
    purpose: str
    quantity: Optional[str] = None
    url: Optional[str] = None
    udl_accommodation: Optional[str] = None  # How it supports different learners

# Enhanced community connections with partnership protocols
class CommunityPartnership(BaseModel):
    partner_type: str  # "expert", "organization", "institution"
    partner_name: str
    role_in_project: str
    interaction_protocols: List[str]  # How students will engage
    authentic_context: str           # Real-world connection
    communication_schedule: str

class CommunityConnection(BaseModel):
    partnerships: List[CommunityPartnership] = []
    field_experiences: List[str] = []
    authentic_audiences: List[str] = []
    real_world_connections: str

class DifferentiationSupport(BaseModel):
    learner_type: str
    strategies: List[str]
    supports: List[str] = []
    udl_alignment: List[UDLSupport] = []
    choice_modifications: List[str] = []

class FamilyEngagement(BaseModel):
    home_connections: List[str] = []
    communication_plan: str
    cultural_assets: List[str] = []
    family_expertise_integration: List[str] = []

# Main PBL Project Model - Enhanced
class PBLProject(BaseModel):
    # Core project information
    title: str
    grade_level: Union[GradeLevel, str]
    duration: str
    driving_question: str
    project_summary: str
    
    # Subject integration with TPACK
    primary_subject: SubjectArea
    secondary_subjects: List[SubjectArea] = []
    steam_focus: STEAMFocus
    technology_integrations: List[TechnologyIntegration] = []
    
    # Enhanced standards and learning goals
    primary_standards: List[Standard]
    secondary_standards: List[Standard] = []
    learning_goals: List[LearningGoal]
    learning_progressions: List[LearningProgression] = []
    
    # HQPBL alignment with detailed scaffolds
    intellectual_challenge: str
    authenticity: str
    public_product: str
    collaboration: CollaborationStructure
    project_management: str
    reflection: List[ReflectionScaffold]
    
    # Enhanced project structure
    project_phases: List[ProjectPhase]
    products_deliverables: Dict[str, List[Product]]
    student_choice_architecture: List[StudentChoice] = []
    
    # Assessment with frequent feedback
    assessment_strategy: Dict[str, List[Assessment]]
    formative_feedback_loops: List[str] = []
    
    # Resources and community
    resources: List[Resource]
    community_connections: CommunityConnection
    
    # Universal design and differentiation
    udl_framework: List[UDLSupport]
    differentiation: List[DifferentiationSupport]
    family_engagement: FamilyEngagement
    
    # Cultural responsiveness and transfer
    community_connections_description: str
    cultural_assets: List[str] = []
    local_relevance: str
    transfer_objectives: List[TransferScaffold] = []

    core_skills_framework: CoreSkillsFramework          # NEW
    skill_assessment_plan: Dict[str, List[SkillAssessment]]  # NEW - skill_area -> assessments
    skill_differentiation: Dict[str, List[str]] = {}    # NEW - skill_area -> supports

# Template and output models remain similar but with enhanced structure
class PBLProjectTemplate(BaseModel):
    grade_level: Union[GradeLevel, str]
    primary_subject: SubjectArea
    topic_focus: str
    duration_weeks: int
    
    # Enhanced customization
    student_interests: List[str] = []
    cultural_context: Optional[str] = None
    community_challenges: List[str] = []
    available_technology: List[str] = []
    local_resources: List[str] = []
    udl_priorities: List[UDLNetwork] = []
    
    # Constraints
    required_standards: List[str] = []
    assessment_preferences: List[AssessmentType] = []
    collaboration_level: ActivityLevel = ActivityLevel.INTERMEDIATE
    transfer_goals: List[str] = []

# Enhanced lesson plan with 5E model and UDL
class LessonPlan(BaseModel):
    title: str
    objectives: List[str]
    duration: str
    grade_level: Union[GradeLevel, str]
    materials_needed: List[str]
    
    # 5E model structure with UDL supports
    engage: Dict[str, Union[str, int, List[str]]]  # description, minutes, udl_supports
    explore: Dict[str, Union[str, int, List[str]]]
    explain: Dict[str, Union[str, int, List[str]]]
    elaborate: Dict[str, Union[str, int, List[str]]]
    evaluate: Dict[str, Union[str, int, List[str]]]
    
    # Enhanced assessment and support
    observation_checklist: List[str] = []
    self_assessment: Optional[str] = None
    peer_feedback: Optional[str] = None
    differentiation_tips: List[str] = []
    extensions: List[str] = []
    udl_accommodations: List[UDLSupport] = []
    
    # Standards and progression
    educational_standards: List[Standard] = []
    learning_progression_focus: Optional[str] = None

class PBLProjectOutput(BaseModel):
    project: PBLProject
    lesson_plans: List[LessonPlan] = []
    teacher_guide: Optional[str] = None
    student_handouts: List[Dict[str, str]] = []
    rubrics: List[Dict[str, Union[str, List]]] = []
    resource_links: List[Dict[str, str]] = []
    reflection_tools: List[Dict[str, str]] = []
    family_communication_templates: List[Dict[str, str]] = []