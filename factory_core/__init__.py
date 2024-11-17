"""
ShortFactory Core Module
"""

from .ai.model_manager import ModelManager
from .ai.style_manager import StyleManager
from .ai.script_generator import ScriptGenerator
from .assets.asset_manager import AssetManager
from .audio.audio_manager import AudioManager
from .config.config_manager import ConfigManager
from .editing.video_editor import VideoEditor
from .factory import ShortFactory, VideoConfig

__version__ = "0.1.0"
__all__ = [
    "ModelManager",
    "StyleManager",
    "ScriptGenerator",
    "AssetManager",
    "AudioManager",
    "ConfigManager",
    "VideoEditor",
    "ShortFactory",
    "VideoConfig",
]
