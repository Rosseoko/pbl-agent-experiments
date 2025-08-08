from enum import Enum
from typing import TypeVar, Type

# ============================================================================
# CORE ENUMS
# ============================================================================

# Type variable for enum with display names
T = TypeVar('T', bound='EnumWithDisplay')

class EnumWithDisplay(str, Enum):
    """Base class for enums that need display names."""
    
    @property
    def display_name(self) -> str:
        """Return a human-readable name for the enum value."""
        return self.value.replace('_', ' ').title()
    
    @classmethod
    def get_display_name(cls: Type[T], value: str) -> str:
        """Get the display name for a given enum value."""
        try:
            return cls(value).display_name
        except ValueError:
            return value  # Return as is if not a valid enum value


class TemplateIntent(EnumWithDisplay):
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


class Duration(EnumWithDisplay):
    SPRINT = "SPRINT"          # 1-3 days
    UNIT = "UNIT"              # 1-4 weeks
    JOURNEY = "JOURNEY"        # 6-12 weeks
    CAMPAIGN = "CAMPAIGN"      # Semester/Year


class SocialStructure(EnumWithDisplay):
    INDIVIDUAL = "INDIVIDUAL"
    COLLABORATIVE = "COLLABORATIVE"
    COMMUNITY_CONNECTED = "COMMUNITY_CONNECTED"
    NETWORKED = "NETWORKED"


class CognitiveComplexity(EnumWithDisplay):
    APPLICATION = "APPLICATION"
    ANALYSIS = "ANALYSIS"
    SYNTHESIS = "SYNTHESIS"
    EVALUATION = "EVALUATION"


class AuthenticityLevel(EnumWithDisplay):
    SIMULATED = "SIMULATED"
    ANCHORED = "ANCHORED"
    APPLIED = "APPLIED"
    IMPACT = "IMPACT"


class ScaffoldingIntensity(EnumWithDisplay):
    GUIDED = "GUIDED"
    FACILITATED = "FACILITATED"
    INDEPENDENT = "INDEPENDENT"
    MENTORED = "MENTORED"


class ProductComplexity(EnumWithDisplay):
    ARTIFACT = "ARTIFACT"
    PORTFOLIO = "PORTFOLIO"
    SYSTEM = "SYSTEM"
    EXPERIENCE = "EXPERIENCE"


class DeliveryMode(EnumWithDisplay):
    FACE_TO_FACE = "FACE_TO_FACE"
    SYNCHRONOUS_REMOTE = "SYNCHRONOUS_REMOTE"
    ASYNCHRONOUS_REMOTE = "ASYNCHRONOUS_REMOTE"
    HYBRID = "HYBRID"


class SubjectArea(EnumWithDisplay):
    SCIENCE = "SCIENCE"
    MATHEMATICS = "MATHEMATICS"
    SOCIAL_STUDIES = "SOCIAL_STUDIES"
    ENGLISH_LANGUAGE_ARTS = "ENGLISH_LANGUAGE_ARTS"
    ARTS = "ARTS"
    TECHNOLOGY = "TECHNOLOGY"
    HEALTH_PE = "HEALTH_PE"
    WORLD_LANGUAGES = "WORLD_LANGUAGES"