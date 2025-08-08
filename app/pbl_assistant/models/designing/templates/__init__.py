# templates/__init__.py
"""
Entry point for all pedagogical templates. These are discovered dynamically by TemplateRegistry.
"""

# core_academic templates
from .core_academic.scientific_inquiry import TEMPLATE as scientific_inquiry_template
from .core_academic.engineering_design import TEMPLATE as engineering_design_template
from .core_academic.mathematical_modeling import TEMPLATE as mathematical_modeling_template
from .core_academic.research_investigation import TEMPLATE as research_investigation_template
from .core_academic.historical_inquiry import TEMPLATE as historical_inquiry_template

# applied_creative templates
from .applied_creative.community_action import TEMPLATE as community_action_template
from .applied_creative.creative_expression import TEMPLATE as creative_expression_template
from .applied_creative.technology_focused import TEMPLATE as technology_focused_template
from .applied_creative.entrepreneurship import TEMPLATE as entrepreneurship_template
from .applied_creative.service_learning import TEMPLATE as service_learning_template

# integration_skill templates
from .integration_skill.interdisciplinary import TEMPLATE as interdisciplinary_template
from .integration_skill.skill_application import TEMPLATE as skill_application_template
from .integration_skill.design_thinking import TEMPLATE as design_thinking_template
from .integration_skill.debate_argumentation import TEMPLATE as debate_argumentation_template

__all__ = [
    "scientific_inquiry_template",
    "engineering_design_template",
    "mathematical_modeling_template",
    "research_investigation_template",
    "historical_inquiry_template",
    "community_action_template",
    "creative_expression_template",
    "technology_focused_template",
    "entrepreneurship_template",
    "service_learning_template",
    "interdisciplinary_template",
    "skill_application_template",
    "design_thinking_template",
    "debate_argumentation_template",
]