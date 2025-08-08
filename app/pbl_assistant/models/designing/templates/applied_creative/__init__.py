# Ensure subpackages are imported so modules within them are loaded
import templates.core_academic
import templates.applied_creative
import templates.integration_skill

# templates/applied_creative/__init__.py
"""
Applied & Creative PBL templates.
"""
from .community_action import TEMPLATE
from .creative_expression import TEMPLATE
from .technology_focused import TEMPLATE
from .entrepreneurship import TEMPLATE
from .service_learning import TEMPLATE

__all__ = [
    "TEMPLATE"
]
