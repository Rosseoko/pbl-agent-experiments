# designing/__init__.py
"""
The root package for the PBL Design system. Exposes core, configuration, and registry subpackages.
"""

__version__ = "0.1.0"

# Import and expose all necessary components from subpackages
from .core import (
    BaseTemplate, Duration, SocialStructure, CognitiveComplexity,
    AuthenticityLevel, ScaffoldingIntensity, ProductComplexity, DeliveryMode
)
from .configuration import *
from .registry import *

# Note: templates are accessed via TemplateRegistry or factory functions

__all__ = [
    # Core components
    'BaseTemplate', 'Duration', 'SocialStructure', 'CognitiveComplexity',
    'AuthenticityLevel', 'ScaffoldingIntensity', 'ProductComplexity', 'DeliveryMode',
    
    # Subpackages
    'core',
    'configuration',
    'registry',
]
