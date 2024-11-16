from abc import ABC, abstractmethod
from typing import Dict, Any, List
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip

class VideoTemplate(ABC):
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize video template.
        
        Args:
            config (Dict[str, Any]): Template configuration
        """
        self.config = config
        self.width = config['dimensions'][0]
        self.height = config['dimensions'][1]
        self.duration = config.get('duration', 60)
        
    @abstractmethod
    def apply_template(
        self,
        clips: List[VideoFileClip],
        audio: AudioFileClip,
        text_content: Dict[str, str]
    ) -> VideoFileClip:
        """
        Apply template to video clips.
        
        Args:
            clips (List[VideoFileClip]): List of video clips
            audio (AudioFileClip): Audio track
            text_content (Dict[str, str]): Text content for overlays
            
        Returns:
            VideoFileClip: Final video with template applied
        """
        pass
    
    def get_template_config(self) -> Dict[str, Any]:
        """
        Get template configuration.
        
        Returns:
            Dict[str, Any]: Template configuration
        """
        return self.config
