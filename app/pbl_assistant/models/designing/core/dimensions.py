# core/dimensions.py
from typing import Dict, List
from pydantic import BaseModel, Field
from .enums import (
    Duration, SocialStructure, CognitiveComplexity,
    AuthenticityLevel, ScaffoldingIntensity,
    ProductComplexity, DeliveryMode
)

# ============================================================================
# DIMENSIONAL CONFIGURATION MODELS (Fixed Definitions)
# ============================================================================

class DurationDefinition(BaseModel):
    """Fixed definition of what each duration means"""
    duration: Duration
    label: str
    description: str
    typical_timeframe: str
    learning_depth: str
    skill_focus: str
    assessment_frequency: str
    reflection_intensity: str
    project_management_complexity: str
    default_scaffolding: ScaffoldingIntensity

class SocialStructureDefinition(BaseModel):
    """Fixed definition of each social structure"""
    structure: SocialStructure
    label: str
    description: str
    typical_group_size: str
    interaction_pattern: str
    accountability_structure: str
    assessment_approach: str
    product_sharing_method: str
    required_teacher_role: str
    compatible_authenticity: List[AuthenticityLevel]
    minimum_scaffolding: ScaffoldingIntensity

class CognitiveComplexityDefinition(BaseModel):
    """Fixed definition of cognitive complexity levels"""
    complexity: CognitiveComplexity
    label: str
    description: str
    bloom_level: str
    thinking_verbs: List[str]
    question_stems: List[str]
    assessment_indicators: List[str]
    prerequisite_skills: List[str]
    professional_alignment: str

class AuthenticityDefinition(BaseModel):
    """Fixed definition of authenticity levels"""
    level: AuthenticityLevel
    label: str
    description: str
    reality_connection: str
    audience_type: str
    tools_and_resources: List[str]
    constraints_and_limitations: List[str]
    stakes_and_consequences: str
    professional_alignment: str

class ScaffoldingDefinition(BaseModel):
    """Fixed definition of scaffolding intensities"""
    intensity: ScaffoldingIntensity
    label: str
    description: str
    teacher_role: str
    student_autonomy_level: str
    decision_making_authority: str
    guidance_frequency: str
    resource_provision: str
    feedback_timing: str
    suitable_for_experience_levels: List[str]

class ProductComplexityDefinition(BaseModel):
    """Fixed definition of product complexity levels"""
    complexity: ProductComplexity
    label: str
    description: str
    creation_scope: str
    maintenance_requirements: str
    collaboration_needs: str
    technical_skills_required: List[str]
    time_investment: str
    assessment_focus: str

class DeliveryModeDefinition(BaseModel):
    """Fixed definition of delivery modes"""
    mode: DeliveryMode
    label: str
    description: str
    technology_requirements: List[str]
    interaction_patterns: List[str]
    assessment_adaptations: List[str]
    scaffolding_modifications: List[str]
    social_structure_impacts: Dict[SocialStructure, str]

class DimensionalRegistry(BaseModel):
    durations: Dict[Duration, DurationDefinition] = Field(default_factory=dict)
    social_structures: Dict[SocialStructure, SocialStructureDefinition] = Field(default_factory=dict)
    cognitive_complexities: Dict[CognitiveComplexity, CognitiveComplexityDefinition] = Field(default_factory=dict)
    authenticity_levels: Dict[AuthenticityLevel, AuthenticityDefinition] = Field(default_factory=dict)
    scaffolding_intensities: Dict[ScaffoldingIntensity, ScaffoldingDefinition] = Field(default_factory=dict)
    product_complexities: Dict[ProductComplexity, ProductComplexityDefinition] = Field(default_factory=dict)
    delivery_modes: Dict[DeliveryMode, DeliveryModeDefinition] = Field(default_factory=dict)

    @classmethod
    def create_default_registry(cls) -> 'DimensionalRegistry':
        registry = cls()
        # Load duration definitions
        registry.durations[Duration.SPRINT] = DurationDefinition(
            duration=Duration.SPRINT,
            label="Sprint (1-3 days)",
            description="Surface exploration with single skill focus",
            typical_timeframe="1-3 class periods",
            learning_depth="Surface level exploration",
            skill_focus="Single skill practice",
            assessment_frequency="Daily check-ins",
            reflection_intensity="Brief exit tickets",
            project_management_complexity="Simple task lists",
            default_scaffolding=ScaffoldingIntensity.GUIDED
        )
        registry.durations[Duration.UNIT] = DurationDefinition(
            duration=Duration.UNIT,
            label="Unit (1-4 weeks)",
            description="Concept mastery and skill development",
            typical_timeframe="2-4 weeks",
            learning_depth="Concept mastery",
            skill_focus="Skill refinement",
            assessment_frequency="Weekly quizzes",
            reflection_intensity="Structured journal entries",
            project_management_complexity="Milestone-based planning",
            default_scaffolding=ScaffoldingIntensity.FACILITATED
        )
        # TODO: load definitions for other dimensions (social_structures, cognitive_complexities, authenticity_levels, scaffolding_intensities, product_complexities, delivery_modes)
        return registry
