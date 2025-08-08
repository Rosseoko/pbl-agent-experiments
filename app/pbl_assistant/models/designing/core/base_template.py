from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pydantic import BaseModel, Field
from .enums import (
    TemplateIntent, SubjectArea,
    Duration, SocialStructure, CognitiveComplexity,
    AuthenticityLevel, ScaffoldingIntensity,
    ProductComplexity, DeliveryMode
)

# Existing Core Models (ESSENTIAL - DO NOT REMOVE)
class EntryEventOption(BaseModel):
    """Single entry event option within a template"""
    type: str
    example: str
    student_response_pattern: str
    question_generation_method: str
    estimated_time: str
    materials_needed: List[str]

class EntryEventFramework(BaseModel):
    """Framework for launching projects"""
    purpose: str
    design_principles: List[str]
    template_options: List[EntryEventOption]
    customization_guidance: str

class MilestoneTemplate(BaseModel):
    """Template for project milestones - agnostic to duration"""
    milestone_name: str
    learning_purpose: str
    core_activities: List[str]
    essential_deliverables: List[str]
    reflection_checkpoints: List[str]
    duration_scaling_notes: str  # Guidance for how this scales with duration

class FormativeAssessmentTool(BaseModel):
    """Formative assessment tool template"""
    tool_name: str
    purpose: str
    implementation_guidance: str
    frequency_recommendations: Dict[Duration, str]
    scaling_guidance: Dict[Duration, str]

class SummativeAssessmentMoment(BaseModel):
    """Summative assessment moment template"""
    moment_name: str
    purpose: str
    typical_timing: str
    assessment_focus: List[str]
    rubric_guidance: str

class ReflectionProtocol(BaseModel):
    """Reflection protocol template"""
    protocol_name: str
    purpose: str
    structure: Optional[List[str]] = None
    timing_guidance: str
    facilitation_notes: str

class AssessmentFramework(BaseModel):
    """Complete assessment framework for a template"""
    formative_tools: List[FormativeAssessmentTool]
    summative_moments: List[SummativeAssessmentMoment]
    reflection_protocols: List[ReflectionProtocol]
    portfolio_guidance: str

class AuthenticAudienceFramework(BaseModel):
    """Framework for authentic audiences"""
    audience_categories: List[str]
    engagement_formats: List[str]
    preparation_requirements: List[str]
    logistical_considerations: List[str]

class CompatibilityMatrix(BaseModel):
    duration_compatible: List[Duration]
    social_structure_compatible: List[SocialStructure]
    cognitive_complexity_range: List[CognitiveComplexity]
    authenticity_compatible: List[AuthenticityLevel]
    scaffolding_compatible: List[ScaffoldingIntensity]
    product_complexity_compatible: List[ProductComplexity]
    delivery_mode_compatible: List[DeliveryMode]

class HQPBLAlignment(BaseModel):
    intellectual_challenge: str
    authenticity: str
    public_product: str
    collaboration: str

# Progressive Education Framework Components
class InquiryFramework(BaseModel):
    """Wonder-driven inquiry structure inspired by Reggio Emilia"""
    what_we_know_prompts: List[str] = Field(default_factory=list, description="Questions to surface prior knowledge")
    what_we_wonder_prompts: List[str] = Field(default_factory=list, description="Curiosity-generating questions")
    what_we_want_to_learn_prompts: List[str] = Field(default_factory=list, description="Learning goal co-creation")
    how_we_might_explore_options: List[str] = Field(default_factory=list, description="Multiple investigation pathways")
    reflection_return_prompts: List[str] = Field(default_factory=list, description="Thinking evolution questions")

class LearningEnvironmentFramework(BaseModel):
    """Environment as third teacher principles"""
    physical_space_invitations: List[str] = Field(default_factory=list, description="Space setups that invite exploration")
    documentation_displays: List[str] = Field(default_factory=list, description="Ways to make thinking visible")
    material_provocations: List[str] = Field(default_factory=list, description="Objects/materials that spark curiosity")
    collaboration_zones: List[str] = Field(default_factory=list, description="Spaces for different group configurations")
    reflection_retreats: List[str] = Field(default_factory=list, description="Quiet processing spaces")

class StudentAgencyFramework(BaseModel):
    """Progressive choice and voice integration"""
    natural_choice_points: List[str] = Field(default_factory=list, description="Meaningful decision opportunities")
    voice_amplification_strategies: List[str] = Field(default_factory=list, description="How all students contribute")
    ownership_transfer_milestones: List[str] = Field(default_factory=list, description="Gradual release moments")
    peer_collaboration_structures: List[str] = Field(default_factory=list, description="Student-to-student support")

class DocumentationFramework(BaseModel):
    """Making learning visible - Reggio inspired"""
    learning_capture_opportunities: List[str] = Field(default_factory=list, description="When/what to document")
    student_thinking_artifacts: List[str] = Field(default_factory=list, description="Evidence of deep understanding")
    process_documentation_methods: List[str] = Field(default_factory=list, description="Journey capture techniques")
    celebration_sharing_formats: List[str] = Field(default_factory=list, description="Ways to honor learning")

class ExpressionPathways(BaseModel):
    """Multiple ways students can demonstrate understanding"""
    visual_expression_options: List[str] = Field(default_factory=list, description="Drawing, photography, infographics")
    kinesthetic_expression_options: List[str] = Field(default_factory=list, description="Building, movement, drama")
    verbal_expression_options: List[str] = Field(default_factory=list, description="Discussion, storytelling, presentation")
    collaborative_expression_options: List[str] = Field(default_factory=list, description="Group projects, peer teaching")
    creative_expression_options: List[str] = Field(default_factory=list, description="Arts integration, innovative formats")

class EmergentLearningSupport(BaseModel):
    """Support for curriculum that can adapt to student interests"""
    pivot_opportunity_indicators: List[str] = Field(default_factory=list, description="Signs learning can shift direction")
    student_interest_amplifiers: List[str] = Field(default_factory=list, description="How to build on passions")
    unexpected_connection_bridges: List[str] = Field(default_factory=list, description="Linking surprising discoveries")
    community_opportunity_integrators: List[str] = Field(default_factory=list, description="Real-world connection points")

# Enhanced Base Template
class BaseTemplate(BaseModel):
    """Base template with implicit progressive education integration"""
    template_id: str = Field(pattern=r'^[a-z_]+$')
    intent: TemplateIntent
    display_name: str
    description: str
    pedagogical_approach: str
    comprehensive_overview: Optional[str] = Field(
        None, 
        description="A comprehensive description of how the project works, including sequence, evaluation, and configuration options"
    )
    
    # Core Template Structure
    driving_question_template: str
    core_learning_cycle: List[str] = Field(min_length=3, max_length=6)
    essential_skills: List[str] = Field(min_length=3)
    required_components: List[str] = Field(min_length=3)
    
    # Subject Integration
    natural_subject_areas: List[SubjectArea]
    cross_curricular_connections: List[str]
    
    # Progressive Education Integration (Optional with defaults)
    inquiry_framework: Optional[InquiryFramework] = Field(default_factory=InquiryFramework)
    learning_environment_framework: Optional[LearningEnvironmentFramework] = Field(default_factory=LearningEnvironmentFramework)
    student_agency_framework: Optional[StudentAgencyFramework] = Field(default_factory=StudentAgencyFramework)
    documentation_framework: Optional[DocumentationFramework] = Field(default_factory=DocumentationFramework)
    expression_pathways: Optional[ExpressionPathways] = Field(default_factory=ExpressionPathways)
    emergent_learning_support: Optional[EmergentLearningSupport] = Field(default_factory=EmergentLearningSupport)
    
    # Existing Template Frameworks
    entry_event_framework: EntryEventFramework
    milestone_templates: List[MilestoneTemplate]
    assessment_framework: AssessmentFramework
    authentic_audience_framework: AuthenticAudienceFramework
    
    # Resources and Tools
    project_management_tools: List[str]
    recommended_resources: List[str]
    technology_suggestions: List[str]
    
    # Standards and Quality
    standards_alignment_examples: Dict[str, List[str]]
    hqpbl_alignment: HQPBLAlignment
    
    # Compatibility
    compatibility_matrix: CompatibilityMatrix
    
    # Implementation Guidance
    teacher_preparation_notes: List[str]
    common_challenges: List[str]
    success_indicators: List[str]
    
    # Teacher Support (Optional with defaults)
    getting_started_essentials: List[str] = Field(
        default_factory=list,
        description="Minimum viable implementation steps"
    )
    when_things_go_wrong: List[str] = Field(
        default_factory=list,
        description="Common pivots and solutions"
    )
    signs_of_success: List[str] = Field(
        default_factory=list,
        description="What thriving learning looks like"
    )
    
    # Additional Teacher Decision-Making Support (Optional with defaults)
    teacher_prep_essentials: List[str] = Field(
        default_factory=list,
        description="Key preparation tasks for teachers before implementation"
    )
    student_readiness: str = Field(
        default="",
        description="Prerequisites and student readiness considerations"
    )
    community_engagement_level: str = Field(
        default="",
        description="Level and type of community connections required"
    )
    assessment_highlights: List[str] = Field(
        default_factory=list,
        description="Key assessment moments and approaches"
    )
    assessment_focus: str = Field(
        default="",
        description="Primary areas of focus for assessment"
    )
    what_success_looks_like: str = Field(
        default="",
        description="Concrete description of successful implementation outcomes"
    )
    
    # Key Elements for Teacher Overview (Optional with defaults)
    final_product_description: str = Field(
        default="",
        description="Clear description of what students will create or produce"
    )
    
    class CoreSkill(BaseModel):
        """Represents a core skill with its application and assessment connection"""
        skill_name: str
        application: str
        assessment_connection: str
    
    core_skills: List[CoreSkill] = Field(
        default_factory=list,
        description="Key skills students will develop with connections to application and assessment"
    )
    
    def is_compatible_with_config(self, config: 'DimensionalConfiguration') -> bool:
        """Check if template is compatible with given dimensional configuration"""
        return (
            config.duration in self.compatibility_matrix.duration_compatible and
            config.social_structure in self.compatibility_matrix.social_structure_compatible and
            config.cognitive_complexity in self.compatibility_matrix.cognitive_complexity_range and
            config.authenticity_level in self.compatibility_matrix.authenticity_compatible and
            config.scaffolding_intensity in self.compatibility_matrix.scaffolding_compatible and
            config.product_complexity in self.compatibility_matrix.product_complexity_compatible and
            config.delivery_mode in self.compatibility_matrix.delivery_mode_compatible
        )