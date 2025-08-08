# Ensure subpackages are imported so modules within them are loaded
import templates.core_academic
import templates.applied_creative
import templates.integration_skill

# templates/core_academic/__init__.py
"""
Core academic PBL templates.
"""
from .scientific_inquiry import TEMPLATE
from .engineering_design import TEMPLATE
from .mathematical_modeling import TEMPLATE
from .research_investigation import TEMPLATE
from .historical_inquiry import TEMPLATE

__all__ = [
    "TEMPLATE"
]
