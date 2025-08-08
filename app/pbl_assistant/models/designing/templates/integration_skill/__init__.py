# Ensure subpackages are imported so modules within them are loaded
import templates.core_academic
import templates.applied_creative
import templates.integration_skill

# templates/integration_skill/__init__.py
"""
Integration & Skill PBL templates.
"""
from .interdisciplinary import TEMPLATE
from .skill_application import TEMPLATE
from .design_thinking import TEMPLATE
from .debate_argumentation import TEMPLATE

__all__ = [
    "TEMPLATE"
]