from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, field_validator
from abc import ABC, abstractmethod

# ============================================================================
# CORE ENUMS
# ============================================================================

class TemplateIntent(str, Enum):
    SCIENTIFIC_INQUIRY = "SCIENTIFIC_INQUIRY"
    ENGINEERING_DESIGN = "ENGINEERING_DESIGN"
    MATHEMATICAL_MODELING = "MATHEMATICAL_MODELING"
    RESEARCH_INVESTIGATION = "RESEARCH_INVESTIGATION"
    HISTORICAL_INQUIRY = "HISTORICAL_INQUIRY"
    COMMUNITY_ACTION = "COMMUNITY_ACTION"
    CREATIVE_EXPRESSION = "CREATIVE_EXPRESSION"
    TECHNOLOGY_FOCUSED = "TECHNOLOGY_FOCUSED"
    ENTREPRENEURSHIP = "ENTREPRENEURSHIP"
    SERVICE_LEARNING = "SERVICE_LEARNING"
    INTERDISCIPLINARY = "INTERDISCIPLINARY"
    SKILL_APPLICATION = "SKILL_APPLICATION"
    DESIGN_THINKING = "DESIGN_THINKING"
    DEBATE_ARGUMENTATION = "DEBATE_ARGUMENTATION"

class Duration(str, Enum):
    SPRINT = "SPRINT"          # 1-3 days
    UNIT = "UNIT"              # 1-4 weeks
    JOURNEY = "JOURNEY"        # 6-12 weeks
    CAMPAIGN = "CAMPAIGN"      # Semester/Year

class SocialStructure(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    COLLABORATIVE = "COLLABORATIVE"
    COMMUNITY_CONNECTED = "COMMUNITY_CONNECTED"
    NETWORKED = "NETWORKED"

class CognitiveComplexity(str, Enum):
    APPLICATION = "APPLICATION"
    ANALYSIS = "ANALYSIS"
    SYNTHESIS = "SYNTHESIS"
    EVALUATION = "EVALUATION"

class AuthenticityLevel(str, Enum):
    SIMULATED = "SIMULATED"
    ANCHORED = "ANCHORED"
    APPLIED = "APPLIED"
    IMPACT = "IMPACT"

class ScaffoldingIntensity(str, Enum):
    GUIDED = "GUIDED"
    FACILITATED = "FACILITATED"
    INDEPENDENT = "INDEPENDENT"
    MENTORED = "MENTORED"

class ProductComplexity(str, Enum):
    ARTIFACT = "ARTIFACT"
    PORTFOLIO = "PORTFOLIO"
    SYSTEM = "SYSTEM"
    EXPERIENCE = "EXPERIENCE"

class DeliveryMode(str, Enum):
    FACE_TO_FACE = "FACE_TO_FACE"
    SYNCHRONOUS_REMOTE = "SYNCHRONOUS_REMOTE"
    ASYNCHRONOUS_REMOTE = "ASYNCHRONOUS_REMOTE"
    HYBRID = "HYBRID"

class SubjectArea(str, Enum):
    SCIENCE = "SCIENCE"
    MATHEMATICS = "MATHEMATICS"
    SOCIAL_STUDIES = "SOCIAL_STUDIES"
    ENGLISH_LANGUAGE_ARTS = "ENGLISH_LANGUAGE_ARTS"
    ARTS = "ARTS"
    TECHNOLOGY = "TECHNOLOGY"
    HEALTH_PE = "HEALTH_PE"
    WORLD_LANGUAGES = "WORLD_LANGUAGES"

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

# ============================================================================
# DIMENSIONAL REGISTRY (Fixed System Configuration)
# ============================================================================

class DimensionalRegistry(BaseModel):
    """Registry of all dimensional definitions - fixed system configuration"""
    durations: Dict[Duration, DurationDefinition] = Field(default_factory=dict)
    social_structures: Dict[SocialStructure, SocialStructureDefinition] = Field(default_factory=dict)
    cognitive_complexities: Dict[CognitiveComplexity, CognitiveComplexityDefinition] = Field(default_factory=dict)
    authenticity_levels: Dict[AuthenticityLevel, AuthenticityDefinition] = Field(default_factory=dict)
    scaffolding_intensities: Dict[ScaffoldingIntensity, ScaffoldingDefinition] = Field(default_factory=dict)
    product_complexities: Dict[ProductComplexity, ProductComplexityDefinition] = Field(default_factory=dict)
    delivery_modes: Dict[DeliveryMode, DeliveryModeDefinition] = Field(default_factory=dict)
    
    @classmethod
    def create_default_registry(cls) -> 'DimensionalRegistry':
        """Create registry with all standard dimensional definitions"""
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
            skill_focus="Skill development and application",
            assessment_frequency="Weekly checkpoints",
            reflection_intensity="Structured reflection protocols",
            project_management_complexity="Milestone tracking",
            default_scaffolding=ScaffoldingIntensity.FACILITATED
        )
        
        # Load social structure definitions
        registry.social_structures[SocialStructure.INDIVIDUAL] = SocialStructureDefinition(
            structure=SocialStructure.INDIVIDUAL,
            label="Individual Work",
            description="Personal mastery and self-directed learning",
            typical_group_size="1",
            interaction_pattern="Teacher-student dyadic",
            accountability_structure="Individual responsibility",
            assessment_approach="Personal portfolio review",
            product_sharing_method="Individual presentations",
            required_teacher_role="Personal coach and mentor",
            compatible_authenticity=[AuthenticityLevel.SIMULATED, AuthenticityLevel.ANCHORED],
            minimum_scaffolding=ScaffoldingIntensity.FACILITATED
        )
        
        registry.social_structures[SocialStructure.COLLABORATIVE] = SocialStructureDefinition(
            structure=SocialStructure.COLLABORATIVE,
            label="Collaborative Teams",
            description="Interdependent team roles with shared accountability",
            typical_group_size="3-5 students",
            interaction_pattern="Peer interdependence",
            accountability_structure="Shared team goals",
            assessment_approach="Individual + team assessment",
            product_sharing_method="Team presentations",
            required_teacher_role="Team facilitator",
            compatible_authenticity=[AuthenticityLevel.SIMULATED, AuthenticityLevel.ANCHORED, AuthenticityLevel.APPLIED],
            minimum_scaffolding=ScaffoldingIntensity.FACILITATED
        )
        
        # Load cognitive complexity definitions
        registry.cognitive_complexities[CognitiveComplexity.APPLICATION] = CognitiveComplexityDefinition(
            complexity=CognitiveComplexity.APPLICATION,
            label="Application",
            description="Using known procedures and practicing skills",
            bloom_level="Level 3 - Application",
            thinking_verbs=["apply", "demonstrate", "use", "implement", "solve"],
            question_stems=["How would you use...", "What would happen if...", "Apply the rule..."],
            assessment_indicators=["Correct procedure execution", "Skill demonstration", "Problem solving"],
            prerequisite_skills=["Conceptual understanding", "Procedural knowledge"]
        )
        
        registry.cognitive_complexities[CognitiveComplexity.ANALYSIS] = CognitiveComplexityDefinition(
            complexity=CognitiveComplexity.ANALYSIS,
            label="Analysis",
            description="Breaking down complex problems and comparing elements",
            bloom_level="Level 4 - Analysis",
            thinking_verbs=["analyze", "compare", "contrast", "examine", "investigate"],
            question_stems=["What are the parts...", "How do these compare...", "What evidence..."],
            assessment_indicators=["Pattern identification", "Relationship analysis", "Evidence evaluation"],
            prerequisite_skills=["Application skills", "Critical thinking basics"]
        )
        
        # Add remaining definitions...
        return registry

# ============================================================================
# BASE TEMPLATE MODELS (Agnostic to Dimensions)
# ============================================================================

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
    """Defines what dimensional configurations work with this template"""
    duration_compatible: List[Duration]
    social_structure_compatible: List[SocialStructure]
    cognitive_complexity_range: List[CognitiveComplexity]
    authenticity_compatible: List[AuthenticityLevel]
    scaffolding_compatible: List[ScaffoldingIntensity]
    product_complexity_compatible: List[ProductComplexity]
    delivery_mode_compatible: List[DeliveryMode]

class HQPBLAlignment(BaseModel):
    """High Quality PBL alignment documentation"""
    intellectual_challenge: str
    authenticity: str
    public_product: str
    collaboration: str
    project_management: str
    reflection: str

# ============================================================================
# BASE TEMPLATE MODEL
# ============================================================================

class BaseTemplate(BaseModel):
    """Base template - completely agnostic to dimensional configurations"""
    template_id: str = Field(pattern=r'^[a-z_]+$')
    intent: TemplateIntent
    display_name: str
    description: str
    pedagogical_approach: str
    
    # Core Template Structure
    driving_question_template: str
    core_learning_cycle: List[str] = Field(min_length=3, max_length=6)
    essential_skills: List[str] = Field(min_length=3)
    required_components: List[str] = Field(min_length=3)
    
    # Subject Integration
    natural_subject_areas: List[SubjectArea]
    cross_curricular_connections: List[str]
    
    # Template Frameworks
    entry_event_framework: EntryEventFramework
    milestone_templates: List[MilestoneTemplate]  # Templates, not configured milestones
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

# ============================================================================
# DIMENSIONAL CONFIGURATION
# ============================================================================

class DimensionalConfiguration(BaseModel):
    """Specific dimensional configuration for a project"""
    duration: Duration
    social_structure: SocialStructure
    cognitive_complexity: CognitiveComplexity
    authenticity_level: AuthenticityLevel
    scaffolding_intensity: ScaffoldingIntensity
    product_complexity: ProductComplexity
    delivery_mode: DeliveryMode
    
    # Configuration metadata
    configuration_rationale: Optional[str] = None
    teacher_preferences: Optional[Dict[str, Any]] = None
    context_constraints: Optional[List[str]] = None

# ============================================================================
# CONFIGURED PROJECT (Result of Template + Dimensions)
# ============================================================================

class ConfiguredMilestone(BaseModel):
    """Milestone configured with specific dimensional parameters"""
    milestone_name: str
    learning_purpose: str
    configured_activities: List[str]
    scaled_deliverables: List[str]
    reflection_checkpoints: List[str]
    estimated_duration: str
    social_organization: str
    scaffolding_level: str

class ConfiguredAssessment(BaseModel):
    """Assessment configured for specific dimensions"""
    assessment_name: str
    purpose: str
    implementation_details: str
    frequency: str
    social_structure_adaptations: str
    scaffolding_adaptations: str

class ConfiguredProject(BaseModel):
    """Complete project resulting from template + dimensional configuration"""
    base_template: BaseTemplate
    dimensional_configuration: DimensionalConfiguration
    
    # Configured Components
    configured_driving_question: str
    configured_milestones: List[ConfiguredMilestone]
    configured_assessments: List[ConfiguredAssessment]
    configured_entry_event: Dict[str, Any]
    configured_authentic_audience: Dict[str, Any]
    
    # Scaled Parameters
    estimated_total_duration: str
    group_organization: str
    teacher_role_description: str
    student_autonomy_level: str
    
    # Implementation Details
    daily_schedule_guidance: Optional[str] = None
    resource_requirements: List[str]
    technology_needs: List[str]
    preparation_checklist: List[str]
    
    @classmethod
    def from_template_and_config(
        cls,
        template: BaseTemplate,
        config: DimensionalConfiguration,
        dimensional_registry: DimensionalRegistry
    ) -> 'ConfiguredProject':
        """Create configured project from template and dimensional configuration"""
        
        if not template.is_compatible_with_config(config):
            raise ValueError(f"Template {template.template_id} not compatible with configuration")
        
        # Configure milestones based on dimensions
        configured_milestones = []
        for milestone_template in template.milestone_templates:
            configured_milestone = ConfiguredMilestone(
                milestone_name=milestone_template.milestone_name,
                learning_purpose=milestone_template.learning_purpose,
                configured_activities=_adapt_activities_to_dimensions(
                    milestone_template.core_activities, config, dimensional_registry
                ),
                scaled_deliverables=_scale_deliverables(
                    milestone_template.essential_deliverables, config, dimensional_registry
                ),
                reflection_checkpoints=milestone_template.reflection_checkpoints,
                estimated_duration=_calculate_milestone_duration(config.duration),
                social_organization=_get_social_organization(config.social_structure, dimensional_registry),
                scaffolding_level=_get_scaffolding_description(config.scaffolding_intensity, dimensional_registry)
            )
            configured_milestones.append(configured_milestone)
        
        return cls(
            base_template=template,
            dimensional_configuration=config,
            configured_driving_question=_adapt_driving_question(template.driving_question_template, config),
            configured_milestones=configured_milestones,
            configured_assessments=_configure_assessments(template.assessment_framework, config, dimensional_registry),
            configured_entry_event=_configure_entry_event(template.entry_event_framework, config),
            configured_authentic_audience=_configure_audience(template.authentic_audience_framework, config),
            estimated_total_duration=dimensional_registry.durations[config.duration].typical_timeframe,
            group_organization=dimensional_registry.social_structures[config.social_structure].typical_group_size,
            teacher_role_description=dimensional_registry.scaffolding_intensities[config.scaffolding_intensity].teacher_role,
            student_autonomy_level=dimensional_registry.scaffolding_intensities[config.scaffolding_intensity].student_autonomy_level,
            resource_requirements=_determine_resources(template, config),
            technology_needs=_determine_technology_needs(template, config),
            preparation_checklist=_generate_preparation_checklist(template, config)
        )

# ============================================================================
# TEMPLATE REGISTRY
# ============================================================================

class TemplateRegistry(BaseModel):
    """Registry for all base templates"""
    templates: Dict[TemplateIntent, BaseTemplate] = Field(default_factory=dict)
    
    def register_template(self, template: BaseTemplate):
        """Register a new base template"""
        self.templates[template.intent] = template
    
    def get_template(self, intent: TemplateIntent) -> Optional[BaseTemplate]:
        """Get template by intent"""
        return self.templates.get(intent)
    
    def get_compatible_templates(self, config: DimensionalConfiguration) -> List[BaseTemplate]:
        """Get all templates compatible with given configuration"""
        return [
            template for template in self.templates.values()
            if template.is_compatible_with_config(config)
        ]
    
    def list_intents(self) -> List[TemplateIntent]:
        """List all registered template intents"""
        return list(self.templates.keys())

# ============================================================================
# HELPER FUNCTIONS FOR CONFIGURATION
# ============================================================================

def _adapt_activities_to_dimensions(
    activities: List[str], 
    config: DimensionalConfiguration, 
    registry: DimensionalRegistry
) -> List[str]:
    """Adapt base activities to specific dimensional configuration"""
    adapted_activities = []
    
    for activity in activities:
        # Adapt based on social structure
        social_def = registry.social_structures[config.social_structure]
        adapted_activity = f"{activity} ({social_def.interaction_pattern})"
        adapted_activities.append(adapted_activity)
    
    return adapted_activities

def _scale_deliverables(
    deliverables: List[str], 
    config: DimensionalConfiguration, 
    registry: DimensionalRegistry
) -> List[str]:
    """Scale deliverables based on duration and product complexity"""
    duration_def = registry.durations[config.duration]
    product_def = registry.product_complexities[config.product_complexity]
    
    scaled_deliverables = []
    for deliverable in deliverables:
        scaled = f"{deliverable} - {duration_def.learning_depth} - {product_def.creation_scope}"
        scaled_deliverables.append(scaled)
    
    return scaled_deliverables

def _calculate_milestone_duration(duration: Duration) -> str:
    """Calculate milestone duration based on overall project duration"""
    duration_map = {
        Duration.SPRINT: "4-8 hours",
        Duration.UNIT: "3-5 days",
        Duration.JOURNEY: "1-2 weeks",
        Duration.CAMPAIGN: "2-4 weeks"
    }
    return duration_map.get(duration, "varies")

def _get_social_organization(social: SocialStructure, registry: DimensionalRegistry) -> str:
    """Get social organization description"""
    return registry.social_structures[social].typical_group_size

def _get_scaffolding_description(scaffolding: ScaffoldingIntensity, registry: DimensionalRegistry) -> str:
    """Get scaffolding description"""
    return registry.scaffolding_intensities[scaffolding].description

def _adapt_driving_question(template: str, config: DimensionalConfiguration) -> str:
    """Adapt driving question template to configuration"""
    # Simple adaptation - in real system would be more sophisticated
    return template.replace("[context]", f"in a {config.duration.value.lower()} project")

def _configure_assessments(
    framework: AssessmentFramework, 
    config: DimensionalConfiguration, 
    registry: DimensionalRegistry
) -> List[ConfiguredAssessment]:
    """Configure assessments based on dimensions"""
    configured = []
    
    for tool in framework.formative_tools:
        configured_assessment = ConfiguredAssessment(
            assessment_name=tool.tool_name,
            purpose=tool.purpose,
            implementation_details=tool.implementation_guidance,
            frequency=tool.frequency_recommendations.get(config.duration, "weekly"),
            social_structure_adaptations=f"Adapted for {config.social_structure.value}",
            scaffolding_adaptations=f"Adapted for {config.scaffolding_intensity.value}"
        )
        configured.append(configured_assessment)
    
    return configured

def _configure_entry_event(framework: EntryEventFramework, config: DimensionalConfiguration) -> Dict[str, Any]:
    """Configure entry event based on dimensions"""
    return {
        "purpose": framework.purpose,
        "recommended_option": framework.template_options[0].type if framework.template_options else "standard",
        "duration_adaptation": f"Scaled for {config.duration.value}",
        "social_adaptation": f"Organized for {config.social_structure.value}"
    }

def _configure_audience(framework: AuthenticAudienceFramework, config: DimensionalConfiguration) -> Dict[str, Any]:
    """Configure authentic audience based on dimensions"""
    return {
        "audience_types": framework.audience_categories,
        "engagement_format": framework.engagement_formats[0] if framework.engagement_formats else "presentation",
        "authenticity_level": config.authenticity_level.value
    }

def _determine_resources(template: BaseTemplate, config: DimensionalConfiguration) -> List[str]:
    """Determine required resources based on template and configuration"""
    base_resources = template.recommended_resources.copy()
    
    # Add configuration-specific resources
    if config.delivery_mode == DeliveryMode.SYNCHRONOUS_REMOTE:
        base_resources.extend(["Video conferencing platform", "Digital collaboration tools"])
    
    return base_resources

def _determine_technology_needs(template: BaseTemplate, config: DimensionalConfiguration) -> List[str]:
    """Determine technology needs"""
    tech_needs = template.technology_suggestions.copy()
    
    if config.delivery_mode in [DeliveryMode.SYNCHRONOUS_REMOTE, DeliveryMode.ASYNCHRONOUS_REMOTE, DeliveryMode.HYBRID]:
        tech_needs.extend(["Reliable internet", "Student devices", "Learning management system"])
    
    return tech_needs

def _generate_preparation_checklist(template: BaseTemplate, config: DimensionalConfiguration) -> List[str]:
    """Generate preparation checklist"""
    checklist = template.teacher_preparation_notes.copy()
    checklist.extend([
        f"Configure for {config.duration.value} duration",
        f"Set up {config.social_structure.value} grouping",
        f"Prepare {config.scaffolding_intensity.value} scaffolding materials"
    ])
    return checklist

# ============================================================================
# SAMPLE TEMPLATE FACTORY
# ============================================================================

def create_community_action_template() -> BaseTemplate:
    """Factory function for Community Action template - 1 of 14"""
    return BaseTemplate(
        template_id="community_action",
        intent=TemplateIntent.COMMUNITY_ACTION,
        display_name="Community Action Project",
        description="Students identify real community problems and develop action plans for meaningful change",
        pedagogical_approach="Problem-based learning with authentic community engagement",
        
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
                "Community problem analysis presentation",
                "Solution prototype demonstration", 
                "Community action plan presentation",
                "Final reflection portfolio"
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
        ]
    )

# ============================================================================
# USAGE EXAMPLE - SYSTEM INITIALIZATION AND PROJECT GENERATION
# ============================================================================

def demonstrate_system_usage():
    """Demonstrate how to use the complete PBL template system"""
    
    # 1. Initialize the dimensional registry with fixed definitions
    dimensional_registry = DimensionalRegistry.create_default_registry()
    
    # 2. Initialize template registry and add templates
    template_registry = TemplateRegistry()
    community_action_template = create_community_action_template()
    template_registry.register_template(community_action_template)
    
    # 3. Create sample dimensional configurations (what would come from project profiling)
    config_option_1 = DimensionalConfiguration(
        duration=Duration.UNIT,
        social_structure=SocialStructure.COLLABORATIVE,
        cognitive_complexity=CognitiveComplexity.ANALYSIS,
        authenticity_level=AuthenticityLevel.APPLIED,
        scaffolding_intensity=ScaffoldingIntensity.FACILITATED,
        product_complexity=ProductComplexity.PORTFOLIO,
        delivery_mode=DeliveryMode.FACE_TO_FACE,
        configuration_rationale="Balanced approach for middle school students with some PBL experience",
        context_constraints=["4-week unit timeline", "classroom-based with community connections"]
    )
    
    config_option_2 = DimensionalConfiguration(
        duration=Duration.JOURNEY,
        social_structure=SocialStructure.COMMUNITY_CONNECTED,
        cognitive_complexity=CognitiveComplexity.SYNTHESIS,
        authenticity_level=AuthenticityLevel.IMPACT,
        scaffolding_intensity=ScaffoldingIntensity.INDEPENDENT,
        product_complexity=ProductComplexity.EXPERIENCE,
        delivery_mode=DeliveryMode.HYBRID,
        configuration_rationale="Advanced approach for experienced students with strong community partnerships",
        context_constraints=["Quarter-long timeline", "hybrid delivery model", "established community partnerships"]
    )
    
    config_option_3 = DimensionalConfiguration(
        duration=Duration.SPRINT,
        social_structure=SocialStructure.COLLABORATIVE,
        cognitive_complexity=CognitiveComplexity.APPLICATION,
        authenticity_level=AuthenticityLevel.ANCHORED,
        scaffolding_intensity=ScaffoldingIntensity.GUIDED,
        product_complexity=ProductComplexity.ARTIFACT,
        delivery_mode=DeliveryMode.FACE_TO_FACE,
        configuration_rationale="Introduction to community action for new PBL students",
        context_constraints=["3-day intensive", "limited community access", "high scaffolding needs"]
    )
    
    # 4. Generate configured projects (the three options that would be presented to teachers)
    try:
        project_option_1 = ConfiguredProject.from_template_and_config(
            community_action_template, config_option_1, dimensional_registry
        )
        
        project_option_2 = ConfiguredProject.from_template_and_config(
            community_action_template, config_option_2, dimensional_registry
        )
        
        project_option_3 = ConfiguredProject.from_template_and_config(
            community_action_template, config_option_3, dimensional_registry
        )
        
        print("✅ Successfully generated three project configuration options!")
        print(f"Option 1: {project_option_1.estimated_total_duration} - {project_option_1.group_organization}")
        print(f"Option 2: {project_option_2.estimated_total_duration} - {project_option_2.group_organization}")
        print(f"Option 3: {project_option_3.estimated_total_duration} - {project_option_3.group_organization}")
        
        return {
            "registry": template_registry,
            "dimensional_registry": dimensional_registry,
            "project_options": [project_option_1, project_option_2, project_option_3]
        }
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return None

# Example of how the system would be used in the multi-agent pipeline
def generate_project_options_for_teacher(
    project_profile: Dict[str, Any],
    template_registry: TemplateRegistry,
    dimensional_registry: DimensionalRegistry
) -> List[ConfiguredProject]:
    """
    This function would be called by the Design Options Generation agent
    after receiving analysis from upstream agents
    """
    
    # 1. Select compatible base templates based on project profile
    # (This logic would analyze teacher intent, constraints, subject areas, etc.)
    compatible_templates = []
    for template in template_registry.templates.values():
        # Example compatibility logic - real system would be more sophisticated
        if any(subject in template.natural_subject_areas for subject in project_profile.get('subject_areas', [])):
            compatible_templates.append(template)
    
    # 2. Generate 3 dimensional configurations based on project profiling
    # (This would use ML/AI to analyze teacher preferences, constraints, student needs, etc.)
    configurations = generate_strategic_configurations(project_profile)
    
    # 3. Create configured project options
    project_options = []
    for i, config in enumerate(configurations[:3]):  # Limit to 3 options
        # Select best template for this configuration
        best_template = select_optimal_template(compatible_templates, config, project_profile)
        
        if best_template and best_template.is_compatible_with_config(config):
            configured_project = ConfiguredProject.from_template_and_config(
                best_template, config, dimensional_registry
            )
            project_options.append(configured_project)
    
    return project_options

def generate_strategic_configurations(project_profile: Dict[str, Any]) -> List[DimensionalConfiguration]:
    """Generate strategic dimensional configurations based on project profiling"""
    # This would contain sophisticated logic to analyze:
    # - Teacher experience and preferences
    # - Student readiness and needs  
    # - Time and resource constraints
    # - Curriculum requirements
    # - School context and culture
    
    # Placeholder implementation - real system would use ML/AI
    return [
        DimensionalConfiguration(
            duration=Duration.UNIT,
            social_structure=SocialStructure.COLLABORATIVE,
            cognitive_complexity=CognitiveComplexity.ANALYSIS,
            authenticity_level=AuthenticityLevel.APPLIED,
            scaffolding_intensity=ScaffoldingIntensity.FACILITATED,
            product_complexity=ProductComplexity.PORTFOLIO,
            delivery_mode=DeliveryMode.FACE_TO_FACE
        )
        # Would generate 2-3 strategic options
    ]

def select_optimal_template(
    templates: List[BaseTemplate], 
    config: DimensionalConfiguration, 
    project_profile: Dict[str, Any]
) -> Optional[BaseTemplate]:
    """Select the optimal template for a given configuration and project profile"""
    # This would contain sophisticated selection logic
    # For now, return first compatible template
    for template in templates:
        if template.is_compatible_with_config(config):
            return template
    return None

if __name__ == "__main__":
    # Demonstrate the complete system
    system_demo = demonstrate_system_usage()
    
    if system_demo:
        print("\n🎯 PBL Template System successfully initialized!")
        print("Ready for multi-agent project generation pipeline.")
    else:
        print("\n❌ System initialization failed.")