"""
Main ShortFactory class integrating all managers and providing high-level video creation API.
"""
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import torch
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from tenacity import retry, stop_after_attempt, wait_exponential

from .ai.model_manager import ModelManager, ModelType
from .ai.style_manager import StyleManager, StyleType
from .assets.asset_manager import AssetManager, AssetType

logger = logging.getLogger(__name__)

class VideoConfig:
    """Video configuration settings."""
    def __init__(
        self,
        topic: str,
        duration: int = 30,
        style: StyleType = StyleType.CINEMATIC,
        platform: str = "youtube_shorts",
        music_mood: str = "upbeat",
        style_strength: float = 0.8,
    ):
        self.topic = topic
        self.duration = duration
        self.style = style
        self.platform = platform
        self.music_mood = music_mood
        self.style_strength = style_strength

class ShortFactory:
    """Main factory class for creating short-form videos."""
    
    def __init__(self):
        # Initialize managers
        self.model_manager = ModelManager()
        self.style_manager = StyleManager()
        self.asset_manager = AssetManager()
        
        # Initialize working directories
        self.output_dir = Path("output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Platform-specific templates
        self.platform_prompts = {
            "youtube_shorts": "Create an engaging YouTube Shorts script about {topic}. "
                            "Focus on quick, attention-grabbing content with clear value "
                            "proposition. Duration: {duration} seconds.",
            "instagram_reels": "Write an Instagram Reels script about {topic}. "
                             "Make it trendy and visually descriptive with potential "
                             "for overlay text. Duration: {duration} seconds.",
            "tiktok": "Create a TikTok script about {topic}. "
                     "Include trending audio/music cues and make it highly engaging "
                     "from the first second. Duration: {duration} seconds.",
        }

    def set_api_key(self, service: str, key: str):
        """Set API key for a service."""
        self.asset_manager.set_api_key(service, key)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def create_video(self, config: VideoConfig) -> Optional[Path]:
        """Create a video using the provided configuration."""
        try:
            # 1. Generate script
            script = await self._generate_script(config)
            if not script:
                raise ValueError("Failed to generate script")
            
            # 2. Extract keywords for video search
            keywords = await self._extract_keywords(script)
            if not keywords:
                raise ValueError("Failed to extract keywords")
            
            # 3. Get video assets
            video_url = await self.asset_manager.get_video(
                query=" ".join(keywords),
                duration=config.duration
            )
            if not video_url:
                raise ValueError("Failed to get video")
            
            # 4. Get music
            music_url = await self.asset_manager.get_music(
                mood=config.music_mood,
                duration=config.duration
            )
            if not music_url:
                raise ValueError("Failed to get music")
            
            # 5. Download assets
            video_path = await self.asset_manager.download_asset(
                video_url, AssetType.VIDEO
            )
            music_path = await self.asset_manager.download_asset(
                music_url, AssetType.MUSIC
            )
            if not video_path or not music_path:
                raise ValueError("Failed to download assets")
            
            # 6. Apply style transfer
            styled_video = await self._apply_style(
                video_path,
                config.style,
                config.style_strength
            )
            if not styled_video:
                raise ValueError("Failed to apply style")
            
            # 7. Compose final video
            output_path = await self._compose_video(
                styled_video,
                music_path,
                script,
                config
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"Video creation failed: {str(e)}")
            return None

    async def _generate_script(self, config: VideoConfig) -> Optional[str]:
        """Generate video script based on topic and platform."""
        prompt_template = self.platform_prompts.get(
            config.platform, self.platform_prompts["youtube_shorts"]
        )
        
        prompt = prompt_template.format(
            topic=config.topic,
            duration=config.duration
        )
        
        return await self.model_manager.generate_text(
            prompt=prompt,
            max_length=200,
            model_type=ModelType.SCRIPT_GEN
        )

    async def _extract_keywords(self, script: str) -> Optional[List[str]]:
        """Extract keywords from script for video search."""
        labels = [
            "landscape", "people", "action", "nature", "urban",
            "technology", "lifestyle", "business", "sports", "food"
        ]
        
        classifications = await self.model_manager.classify_text(script, labels)
        if not classifications:
            return None
            
        # Get top 3 categories
        sorted_labels = sorted(
            classifications.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [label for label, _ in sorted_labels[:3]]

    async def _apply_style(
        self,
        video_path: Path,
        style: StyleType,
        strength: float
    ) -> Optional[VideoFileClip]:
        """Apply style transfer to video."""
        try:
            # Load video
            video = VideoFileClip(str(video_path))
            
            # Convert to frames
            frames = torch.tensor(list(video.iter_frames()))
            
            # Apply style
            styled_frames = await self.style_manager.apply_style(
                frames=frames,
                style_type=style,
                strength=strength
            )
            
            if styled_frames is None:
                return None
            
            # Convert back to video
            styled_video = VideoFileClip(
                None,
                audio=False,
                fps=video.fps,
                duration=video.duration
            )
            styled_video.frames = list(styled_frames.numpy())
            
            return styled_video
            
        except Exception as e:
            logger.error(f"Style transfer failed: {str(e)}")
            return None

    async def _compose_video(
        self,
        video: VideoFileClip,
        music_path: Path,
        script: str,
        config: VideoConfig
    ) -> Optional[Path]:
        """Compose final video with music and text overlays."""
        try:
            # Load music
            music = AudioFileClip(str(music_path))
            
            # Adjust music duration
            if music.duration > video.duration:
                music = music.subclip(0, video.duration)
            else:
                music = music.loop(duration=video.duration)
            
            # Set music volume
            music = music.volumex(0.3)
            
            # Add music to video
            video = video.set_audio(music)
            
            # Generate text overlays (simplified for now)
            # TODO: Add more sophisticated text animations
            lines = script.split("\n")
            text_clips = []
            
            # Save final video
            output_path = self.output_dir / f"{hash(config.topic)}.mp4"
            video.write_videofile(
                str(output_path),
                codec="libx264",
                audio_codec="aac",
                fps=30
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"Video composition failed: {str(e)}")
            return None

    def clear_cache(self):
        """Clear all caches."""
        self.model_manager.clear_cache()
        self.style_manager.clear_cache()
        self.asset_manager.clear_cache()
        logger.info("All caches cleared")
