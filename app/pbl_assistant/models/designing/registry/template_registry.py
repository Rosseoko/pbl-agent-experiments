"""
Manages discovery and retrieval of all BaseTemplate instances in the system.
"""
import pkgutil
import importlib
from typing import Dict, List
from app.pbl_assistant.models.designing.core.base_template import BaseTemplate
from app.pbl_assistant.models.designing.core.dimensions import DimensionalRegistry

class TemplateRegistry:
    """
    Singleton registry that holds all loaded BaseTemplate objects
    and a shared DimensionalRegistry.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TemplateRegistry, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.registry = DimensionalRegistry.create_default_registry()
        self._templates: Dict[str, BaseTemplate] = {}
        self._load_templates()

    def _load_templates(self):
        """
        Dynamically import all modules under the `templates` package
        and register any that expose a `TEMPLATE` attribute.
        """
        import templates
        for finder, module_name, ispkg in pkgutil.walk_packages(templates.__path__, templates.__name__ + "."):
            module = importlib.import_module(module_name)
            template = getattr(module, "TEMPLATE", None)
            if isinstance(template, BaseTemplate):
                self.register(template)

    def register(self, template: BaseTemplate) -> None:
        """
        Add a BaseTemplate instance to the registry.
        """
        self._templates[template.template_id] = template

    def get_template(self, template_id: str) -> BaseTemplate:
        """
        Retrieve a template by its unique ID.
        """
        return self._templates[template_id]

    def list_templates(self) -> List[BaseTemplate]:
        """
        Return all registered templates.
        """
        return list(self._templates.values())

    def find_by_intent(self, intent: str) -> List[BaseTemplate]:
        """
        Return all templates matching the given pedagogical intent.
        """
        return [t for t in self._templates.values() if t.intent == intent]

