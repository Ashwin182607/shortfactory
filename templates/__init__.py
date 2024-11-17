"""
Video Templates Module
"""

from .base_template import BaseTemplate
from .ai_dynamic_template import AIDynamicTemplate
from .dynamic_template import DynamicTemplate
from .minimal_template import MinimalTemplate
from .modern_template import ModernTemplate

__version__ = "0.1.0"
__all__ = [
    "BaseTemplate",
    "AIDynamicTemplate",
    "DynamicTemplate",
    "MinimalTemplate",
    "ModernTemplate",
]
