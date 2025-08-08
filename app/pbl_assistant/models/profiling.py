from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Dict, Union, Any
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
    response: str = Field(default="", description='The response to give back to the user if they did not give all the necessary details for their project')
    all_details_given: bool = Field(default=False, description='True if the user has given all the necessary details, otherwise false')
    
    topic: Optional[str] = Field(None, description="The main topic or subject of the project")
    grade_level: Optional[Union[GradeLevel, str]] = Field(None, description="Grade level of students")
    duration_preference: Optional[str] = Field(None, description="Preferred duration of the project")

    class_profile: str = Field(default="", description='The class profile, the details about class context: technology access, location, class size, etc.')

    # Language information
    original_language: Optional[str] = Field(
        None,
        description="Original language of the teacher's request if not English"
    )
    original_utterance: Optional[str] = Field(
        None,
        description="Original text of the teacher's request in their language"
    )
    translation: Optional[str] = Field(
        None,
        description="Translation of the teacher's request in English"
    )
    # Optional
    age_range: Optional[Dict[str, int]] = Field(
        None,
        description="Age range of students (min/max)"
    )

    # Core Intent Detection - MADE OPTIONAL
    primary_intent: Optional[ProjectIntent] = Field(None, description="Primary project intent")
    secondary_intents: List[ProjectIntent] = Field(default_factory=list)
    content_area_focus: Optional[ContentArea] = Field(None, description="Main content area focus")
    learning_outcomes: List[str] = Field(default_factory=list)

    # STEM Integration Indicators
    requires_experimentation: bool = Field(False, description="Lab work, testing needed")
    involves_data_collection: bool = Field(False, description="Surveys, measurements, observations")
    needs_mathematical_analysis: bool = Field(False, description="Calculations, graphing, statistics")
    includes_design_challenge: bool = Field(False, description="Building, creating, prototyping")
    uses_technology_tools: bool = Field(False, description="Software, apps, digital creation")
    
    # Learning Approach Indicators
    community_connection_desired: bool = Field(False, description="Real audience, local relevance")
    hands_on_emphasis: bool = Field(False, description="Maker activities, manipulatives")
    research_intensive: bool = Field(False, description="Reading, investigating, citing sources")
    presentation_focused: bool = Field(False, description="Communication, public speaking")
    collaborative_emphasis: bool = Field(False, description="Group work essential")
    
    # Constraint Detection
    materials_mentioned: bool = Field(False, description="Using these materials")
    resource_limitations_mentioned: bool = Field(False, description="We don't have computers")
    time_constraints_noted: bool = Field(False, description="Only have 3 weeks")
    assessment_requirements: List[str] = Field(default_factory=list)
    cultural_considerations: List[str] = Field(default_factory=list)
    
    # Extracted Keywords/Phrases
    implicit_goals: List[str] = Field(default_factory=list, description="Goals teacher didn't explicitly state")

    # Class Interests
    class_interests: List[str] = Field(default_factory=list, description="When the teacher includes specific classroom interests")

    # Standards
    standard_codes: List[str] = Field(default_factory=list, description="List of standard codes when the teacher requests specific standards")

    # Real world exploration
    real_world_exploration: bool = Field(False, description="Whether project involves real world exploration")
    places_to_visit: List[str] = Field(default_factory=list)

    # Skills to develop
    skills_to_develop: List[str] = Field(default_factory=list)

    # End product
    end_product: Optional[str] = Field(None, description="Expected end product")
    
    # Iterative emphasis flag
    iterative_emphasis: bool = Field(
        False,
        description="Whether the project should emphasize iterative development and refinement"
    )
    
    # Interdisciplinary emphasis flag
    interdisciplinary_emphasis: bool = Field(
        False,
        description="Whether the project should emphasize interdisciplinary connections"
    )

    
#Class Profile Models
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


###############################
#Simplier class profile

    
###############################
#Standards agent get_standards
# Core Enums (keep these simple)
class StandardType(str, Enum):
    NGSS = 'ngss'
    CCSS_MATH = 'ccss_math'
    CCSS_ELA = 'ccss_ela'
    NCSS = 'ncss'
    OTHER = 'other'

class BloomLevel(str, Enum):
    REMEMBER = 'remember'
    UNDERSTAND = 'understand'
    APPLY = 'apply'
    ANALYZE = 'analyze'
    EVALUATE = 'evaluate'
    CREATE = 'create'

class DepthOfKnowledge(str, Enum):
    DOK_1 = 'recall'
    DOK_2 = 'skill_concept'
    DOK_3 = 'strategic_thinking'
    DOK_4 = 'extended_thinking'

class ContextualStandard(BaseModel):
    code: str = Field(..., min_length=3, description="Standard code")
    type: StandardType = Field(default=StandardType.OTHER, description="Type of standard")
    description: str = Field(..., min_length=20, description="Description of the standard")
    grade_level: str = Field(..., description="Grade level for this standard")
    is_valid: bool = Field(default=True, description="Whether this standard is valid")
    primary_bloom_level: BloomLevel = Field(default=BloomLevel.APPLY, description="Primary Bloom's level")
    dok_level: DepthOfKnowledge = Field(default=DepthOfKnowledge.DOK_2, description="Depth of Knowledge level")
    project_specific_vocabulary: List[str] = Field(
        default_factory=list, 
        description="List of project-specific vocabulary terms"
    )

class StandardsAlignment(BaseModel):
    """Container for aligned educational standards with related metadata."""
    standards: List[ContextualStandard] = Field(..., min_items=1, description="List of standards in this alignment")
    prerequisites: List[str] = Field(
        default_factory=list, 
        description="List of prerequisite knowledge or skills"
    )
    cross_curricular_connections: List[str] = Field(
        default_factory=list, 
        description="List of connections to other subjects"
    )
    alignment_confidence: float = Field(
        default=0.8, 
        ge=0.0, 
        le=1.0,
        description="Confidence score for the alignment (0.0 to 1.0)"
    )
    validation_issues: List[str] = Field(
        default_factory=list,
        description="List of any validation issues found"
    )
    
    @property
    def primary_standard(self) -> Optional[ContextualStandard]:
        """Get the first standard as the primary standard."""
        return self.standards[0] if self.standards else None
############
#Knowledge Graph Agent

# Simplified Result Model - Focus on what teachers actually need
class KnowledgeGraphResult(BaseModel):
    """Teacher-focused KG insights for PBL planning"""
    
    # Core info
    standard_code: str
    standard_description: str
    
    # The connections that matter for PBL
    project_topics: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Topics from KG that connect to the project"
    )
    
    cross_subject_connections: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Other standards that naturally integrate"
    )
    
    real_world_applications: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="SDG connections showing real-world relevance"
    )
    #important SDG connections
    
    curriculum_resources: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Existing resources that support this standard"
    )
    
    # Teacher implementation ideas
    pbl_integration_ideas: List[str] = Field(
        default_factory=list,
        description="Specific ways to use this standard in the project"
    )
    
    # Simple confidence score
    relevance_confidence: float = 0.9

###Design options project
# Input Model
class ProjectDesignContext(BaseModel):
    project_profile: ProjectDetails
    standards_alignment: StandardsAlignment
    kg_insights: KnowledgeGraphResult
    class_profile: str
    

# Output Models
class ProjectOption(BaseModel):
    title: str = ""
    focus_approach: str = ""
    driving_question: str = ""
    end_product: str = Field("", description="Clear description of what students will create or produce")
    key_skills: List[str] = Field(default_factory=list)
    learning_objectives: List[str] = Field(default_factory=list)
    key_activities: List[str] = Field(default_factory=list)
    assessment_highlights: List[str] = Field(default_factory=list)
    assessment_summary: str = Field("", description="Brief overview of assessment approach")
    differentiation_notes: str = ""
    template_id: str                # ← new
    template_name: str                # ← new
    template_rationale: str         # ← new

class ProjectOptionsResult(BaseModel):
    user_selected_option: Optional[int] = Field(
        None, description="Index of user's selected project option (0, 1, or 2)"
    )
    selection_complete: bool = Field(
        False, description="True when user has made a valid selection"
    )
    response: str = Field(
        "", description="User-facing progress updates"
    )
    #selected_template: str
    #template_rationale: str
    project_options: List[ProjectOption]
    configuration_details: Dict[str, Any]  # Changed from Dict[str, str]