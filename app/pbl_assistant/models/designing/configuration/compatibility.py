# configuration/compatibility.py
from typing import List
from app.pbl_assistant.models.designing.core.base_template import BaseTemplate
from .dimensional_config import DimensionalConfiguration
from app.pbl_assistant.models.designing.core.dimensions import DimensionalRegistry


def is_config_compatible(
    template: BaseTemplate,
    config: DimensionalConfiguration
) -> bool:
    """
    Check whether the given configuration is allowed by the template's compatibility matrix.
    """
    return template.is_compatible_with_config(config)


def filter_compatible_configs(
    template: BaseTemplate,
    configs: List[DimensionalConfiguration]
) -> List[DimensionalConfiguration]:
    """
    From a list of configurations, return only those compatible with the template.
    """
    return [c for c in configs if is_config_compatible(template, c)]


def validate_config_for_template(
    template: BaseTemplate,
    config: DimensionalConfiguration,
    registry: DimensionalRegistry
) -> None:
    """
    Raise informative errors if config violates registry or template rules.
    """
    errors = []
    # Validate via template compatibility
    if not is_config_compatible(template, config):
        errors.append("Configuration values conflict with template compatibility matrix.")
    # Validate each axis against registry definitions
    if config.duration not in registry.durations:
        errors.append(f"Unknown duration: {config.duration}")
    # Additional axis checks could be added here...
    
    if errors:
        raise ValueError("Invalid configuration: " + "; ".join(errors))
