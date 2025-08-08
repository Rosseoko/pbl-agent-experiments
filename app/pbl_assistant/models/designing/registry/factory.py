# registry/factory.py
"""
Convenience functions for fetching templates from the global registry.
"""
from typing import List
from app.pbl_assistant.models.designing.core.base_template import BaseTemplate
from .template_registry import TemplateRegistry


def get_template_by_intent(intent: str) -> List[BaseTemplate]:
    """
    Return all registered templates matching a specific intent.
    """
    registry = TemplateRegistry()
    return registry.find_by_intent(intent)


def list_all_templates() -> List[BaseTemplate]:
    """
    List every template available in the system.
    """
    registry = TemplateRegistry()
    return registry.list_templates()