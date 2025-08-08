# core/__init__.py
from .enums import *
from .dimensions import *
from .base_template import *

# Explicitly import and expose all necessary components
from .enums import (
    Duration, SocialStructure, CognitiveComplexity,
    AuthenticityLevel, ScaffoldingIntensity, ProductComplexity, DeliveryMode
)

from .base_template import BaseTemplate

__all__ = [
    'Duration', 'SocialStructure', 'CognitiveComplexity',
    'AuthenticityLevel', 'ScaffoldingIntensity', 'ProductComplexity', 
    'DeliveryMode', 'BaseTemplate'
]