"""
Utility Functions Module
"""

from .asset_sourcing import AssetSourcer
from .music_manager import MusicManager
from .script_generator import ScriptGenerator
from .text_effects import TextEffects
from .tts import TextToSpeech

__version__ = "0.1.0"
__all__ = [
    "AssetSourcer",
    "MusicManager",
    "ScriptGenerator",
    "TextEffects",
    "TextToSpeech",
]
