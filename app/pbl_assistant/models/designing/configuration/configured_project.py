
from pydantic import BaseModel, Field
from typing import List
from app.pbl_assistant.models.designing.core.base_template import BaseTemplate
from .dimensional_config import DimensionalConfiguration

class ConfiguredProject(BaseModel):
    """
    A fully instantiated project: a base template paired with specific dimension choices.
    """
    template: BaseTemplate = Field(..., description="Base PBL template")
    config: DimensionalConfiguration = Field(..., description="Chosen dimension configuration")
    title: str = Field(..., description="Generated project title")
    driving_question: str = Field(..., description="Generated driving question")
    key_activities: List[str] = Field(..., description="Sequence of key student activities")
    assessment_highlights: List[str] = Field(..., description="Main assessment checkpoints or products")
    differentiation_notes: str = Field(..., description="Notes on how to differentiate for varied learners")

    def summarize(self) -> str:
        """
        Returns a brief summary combining title and core configuration details.
        """
        config_desc = self.config.describe()
        return f"{self.title} ({config_desc})\nDriving Question: {self.driving_question}"