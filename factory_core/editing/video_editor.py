"""
Video Editor for composing and editing videos with effects.
"""
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,
        concatenate_videoclips, vfx
    )
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    logging.warning("MoviePy not found. Video editing will be disabled.")

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logging.warning("OpenCV not found. Some video effects will be limited.")

logger = logging.getLogger(__name__)

class VideoEditor:
    """Handles video editing and composition."""
    
    def __init__(self):
        """Initialize video editor."""
        self.cache_dir = Path(__file__).parent.parent.parent / ".cache/video"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Default text styles
        self.text_styles = {
            "title": {
                "font": "Arial",
                "fontsize": 70,
                "color": "white",
                "stroke_color": "black",
                "stroke_width": 2,
            },
            "subtitle": {
                "font": "Arial",
                "fontsize": 50,
                "color": "white",
                "stroke_color": "black",
                "stroke_width": 1,
            },
            "caption": {
                "font": "Arial",
                "fontsize": 40,
                "color": "white",
                "stroke_color": "black",
                "stroke_width": 1,
            }
        }
    
    def compose_video(
        self,
        video_clips: List[Union[str, Path]],
        audio_path: Optional[Union[str, Path]] = None,
        text_overlays: Optional[List[Dict]] = None,
        transitions: Optional[List[str]] = None,
        output_path: Optional[Path] = None,
        resolution: Tuple[int, int] = (1080, 1920),  # Default to 9:16 ratio
        fps: int = 30
    ) -> Path:
        """Compose a video with audio and effects."""
        if not MOVIEPY_AVAILABLE:
            raise RuntimeError("Video editing is not available. Please install moviepy.")
        
        # Load video clips
        clips = [VideoFileClip(str(clip)).resize(resolution) for clip in video_clips]
        
        # Apply transitions
        if transitions:
            final_clips = []
            for i, clip in enumerate(clips[:-1]):
                final_clips.append(clip)
                transition = transitions[i % len(transitions)]
                if transition == "fade":
                    final_clips[-1] = final_clips[-1].crossfadein(1.0)
                elif transition == "slide":
                    final_clips[-1] = final_clips[-1].set_position(("center", "center"))
            final_clips.append(clips[-1])
            video = concatenate_videoclips(final_clips)
        else:
            video = concatenate_videoclips(clips)
        
        # Add audio if provided
        if audio_path:
            audio = AudioFileClip(str(audio_path))
            video = video.set_audio(audio)
        
        # Add text overlays
        if text_overlays:
            text_clips = []
            for overlay in text_overlays:
                style = self.text_styles[overlay.get("style", "caption")]
                text_clip = TextClip(
                    overlay["text"],
                    font=style["font"],
                    fontsize=style["fontsize"],
                    color=style["color"],
                    stroke_color=style["stroke_color"],
                    stroke_width=style["stroke_width"]
                )
                
                # Position the text
                position = overlay.get("position", ("center", "center"))
                start_time = overlay.get("start_time", 0)
                end_time = overlay.get("end_time", video.duration)
                
                text_clip = (
                    text_clip
                    .set_position(position)
                    .set_start(start_time)
                    .set_end(end_time)
                )
                
                text_clips.append(text_clip)
            
            # Combine video with text overlays
            video = CompositeVideoClip([video] + text_clips)
        
        # Save the final video
        if output_path is None:
            output_path = self.cache_dir / "output.mp4"
        
        video.write_videofile(
            str(output_path),
            fps=fps,
            codec="libx264",
            audio_codec="aac"
        )
        
        # Clean up
        video.close()
        for clip in clips:
            clip.close()
        
        return output_path
    
    def apply_effect(
        self,
        video_path: Path,
        effect: str,
        params: Optional[Dict] = None,
        output_path: Optional[Path] = None
    ) -> Path:
        """Apply a video effect."""
        if not MOVIEPY_AVAILABLE:
            raise RuntimeError("Video effects are not available. Please install moviepy.")
        
        video = VideoFileClip(str(video_path))
        
        # Apply the effect
        if effect == "brightness":
            video = video.fx(vfx.colorx, params.get("factor", 1.5))
        elif effect == "contrast":
            video = video.fx(vfx.lum_contrast, params.get("contrast", 0.5))
        elif effect == "speed":
            video = video.fx(vfx.speedx, params.get("factor", 1.5))
        elif effect == "mirror":
            video = video.fx(vfx.mirror_x)
        elif effect == "reverse":
            video = video.fx(vfx.time_mirror)
        
        # Save the processed video
        if output_path is None:
            output_path = self.cache_dir / f"effect_{effect}_{video_path.name}"
        
        video.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac"
        )
        
        # Clean up
        video.close()
        
        return output_path
    
    def clear_cache(self):
        """Clear video cache."""
        if os.path.exists(self.cache_dir):
            for file in os.listdir(self.cache_dir):
                os.remove(self.cache_dir / file)
            logger.info("Video cache cleared")
