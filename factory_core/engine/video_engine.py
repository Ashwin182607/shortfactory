from typing import Dict, List, Optional, Type, Union
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
from ..ai.script_generator import ScriptGenerator
from ...templates.base_template import VideoTemplate
from ...utils.asset_sourcing import AssetManager
from ...utils.music_manager import MusicManager
import logging

logger = logging.getLogger(__name__)

class VideoEngine:
    """Core video creation engine."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.script_generator = ScriptGenerator()
        self.asset_manager = AssetManager()
        self.music_manager = MusicManager()
    
    def create_video(
        self,
        template: Type[VideoTemplate],
        config: Dict,
        script: Union[str, Dict[str, str]],
        quality: str = "Standard",
        platforms: List[str] = None,
        **kwargs
    ) -> str:
        """
        Create a video using the specified template and configuration.
        
        Args:
            template: Video template class
            config: Template configuration
            script: Video script (string or dict)
            quality: Video quality ("Draft", "Standard", "High Quality")
            platforms: Target platforms
            **kwargs: Additional arguments
            
        Returns:
            str: Path to the generated video
        """
        try:
            # Initialize template
            video_template = template(config)
            
            # Process script
            if isinstance(script, str):
                script_dict = self.script_generator.generate_script(script)
            else:
                script_dict = script
            
            # Get video duration
            duration = config.get('duration', 60)
            
            # Source assets
            logger.info("Sourcing video assets...")
            keywords = self.script_generator.get_keywords(script_dict)
            video_clips = self.asset_manager.source_video_clips(
                keywords,
                duration=duration,
                quality=quality
            )
            
            # Source music
            logger.info("Sourcing background music...")
            music = self.music_manager.find_music(
                style=kwargs.get('music_style', 'Energetic'),
                duration=duration
            )
            
            # Create video
            logger.info("Creating video with template...")
            final_video = video_template.apply_template(
                clips=video_clips,
                audio=music,
                text_content=script_dict
            )
            
            # Export for each platform
            output_paths = []
            for platform in (platforms or ["YouTube Shorts"]):
                output_path = self._export_for_platform(
                    final_video,
                    platform,
                    quality
                )
                output_paths.append(output_path)
            
            return output_paths[0]  # Return first video path
            
        except Exception as e:
            logger.error(f"Error creating video: {str(e)}")
            raise
    
    def _export_for_platform(
        self,
        video: VideoFileClip,
        platform: str,
        quality: str
    ) -> str:
        """Export video with platform-specific settings."""
        # Platform-specific dimensions
        dimensions = {
            "YouTube Shorts": (1080, 1920),
            "Instagram Reels": (1080, 1920),
            "TikTok": (1080, 1920)
        }
        
        # Quality settings
        quality_settings = {
            "Draft": {"bitrate": "1000k", "fps": 24},
            "Standard": {"bitrate": "2500k", "fps": 30},
            "High Quality": {"bitrate": "5000k", "fps": 60}
        }
        
        # Resize video if needed
        target_size = dimensions.get(platform, (1080, 1920))
        if video.size != target_size:
            video = video.resize(target_size)
        
        # Set output path
        output_dir = os.path.join("output", platform.lower().replace(" ", "_"))
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(
            output_dir,
            f"video_{int(time.time())}.mp4"
        )
        
        # Export with quality settings
        settings = quality_settings[quality]
        video.write_videofile(
            output_path,
            fps=settings["fps"],
            bitrate=settings["bitrate"],
            codec="libx264",
            audio_codec="aac"
        )
        
        return output_path
