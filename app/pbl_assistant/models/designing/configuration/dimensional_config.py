from pydantic import BaseModel, Field
from typing import Optional
from app.pbl_assistant.models.designing.core.enums import (
    Duration,
    SocialStructure,
    CognitiveComplexity,
    AuthenticityLevel,
    ScaffoldingIntensity,
    ProductComplexity,
    DeliveryMode
)

# ============================================================================
# DIMENSIONAL CONFIGURATION
# ============================================================================

class DimensionalConfiguration(BaseModel):
    """
    Represents a specific choice on each PBL design dimension.
    """
    duration: Duration = Field(..., description="Selected project duration")
    social_structure: SocialStructure = Field(..., description="Student grouping configuration")
    cognitive_complexity: CognitiveComplexity = Field(..., description="Bloom's level of thinking required")
    authenticity_level: AuthenticityLevel = Field(..., description="Real-world connection intensity")
    scaffolding_intensity: ScaffoldingIntensity = Field(..., description="Level of teacher support")
    product_complexity: ProductComplexity = Field(..., description="Sophistication of student-created artifact")
    delivery_mode: DeliveryMode = Field(..., description="Mode of delivery: F2F, remote, hybrid")
    
    def describe(self) -> str:
        """
        Return a human-readable summary of the configuration.
        """
        return (
            f"Duration: {self.duration.value}, "
            f"Social: {self.social_structure.value}, "
            f"Cognitive: {self.cognitive_complexity.value}, "
            f"Authenticity: {self.authenticity_level.value}, "
            f"Scaffolding: {self.scaffolding_intensity.value}, "
            f"Product: {self.product_complexity.value}, "
            f"Delivery: {self.delivery_mode.value}"
        )