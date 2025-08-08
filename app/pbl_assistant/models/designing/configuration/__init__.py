# Expose configuration package classes and functions
from .dimensional_config import DimensionalConfiguration
from .configured_project import ConfiguredProject
from .compatibility import (
    is_config_compatible,
    filter_compatible_configs,
    validate_config_for_template
)
