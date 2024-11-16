"""
Text Effects Manager for handling text overlays and animations.
"""
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from moviepy.editor import (
    TextClip,
    VideoFileClip,
    CompositeVideoClip,
    ColorClip,
    ImageClip,
)
from moviepy.video.tools.segmenting import findObjects
from moviepy.video.fx.all import fadein, fadeout, resize

logger = logging.getLogger(__name__)

class TextEffect(Enum):
    FADE = "fade"
    SLIDE = "slide"
    TYPEWRITER = "typewriter"
    HIGHLIGHT = "highlight"
    BOUNCE = "bounce"
    WAVE = "wave"
    GLITCH = "glitch"
    GRADIENT = "gradient"

class TextPosition(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    CUSTOM = "custom"

class TextEffectsManager:
    """Manages text overlays and animations for videos."""
    
    def __init__(self):
        self.default_font = "Helvetica-Bold"
        self.default_fontsize = 36
        self.default_color = 'white'
        self.default_stroke_color = 'black'
        self.default_stroke_width = 2

    def create_text_clip(
        self,
        text: str,
        effect: TextEffect,
        position: TextPosition,
        duration: float,
        start_time: float = 0,
        custom_position: Tuple[int, int] = None,
        font: str = None,
        fontsize: int = None,
        color: str = None,
        stroke_color: str = None,
        stroke_width: int = None,
    ) -> TextClip:
        """Create a text clip with the specified effect."""
        # Create base text clip
        txt_clip = TextClip(
            text,
            font=font or self.default_font,
            fontsize=fontsize or self.default_fontsize,
            color=color or self.default_color,
            stroke_color=stroke_color or self.default_stroke_color,
            stroke_width=stroke_width or self.default_stroke_width,
        )
        
        # Set duration
        txt_clip = txt_clip.set_duration(duration)
        
        # Apply effect
        if effect == TextEffect.FADE:
            txt_clip = self._apply_fade_effect(txt_clip)
        elif effect == TextEffect.SLIDE:
            txt_clip = self._apply_slide_effect(txt_clip, position)
        elif effect == TextEffect.TYPEWRITER:
            txt_clip = self._apply_typewriter_effect(txt_clip)
        elif effect == TextEffect.HIGHLIGHT:
            txt_clip = self._apply_highlight_effect(txt_clip)
        elif effect == TextEffect.BOUNCE:
            txt_clip = self._apply_bounce_effect(txt_clip)
        elif effect == TextEffect.WAVE:
            txt_clip = self._apply_wave_effect(txt_clip)
        elif effect == TextEffect.GLITCH:
            txt_clip = self._apply_glitch_effect(txt_clip)
        elif effect == TextEffect.GRADIENT:
            txt_clip = self._apply_gradient_effect(txt_clip)
        
        # Set position
        position_func = self._get_position_function(
            position, custom_position, txt_clip
        )
        txt_clip = txt_clip.set_position(position_func)
        
        # Set start time
        txt_clip = txt_clip.set_start(start_time)
        
        return txt_clip

    def _apply_fade_effect(self, clip: TextClip) -> TextClip:
        """Apply fade in/out effect."""
        return clip.fadein(0.5).fadeout(0.5)

    def _apply_slide_effect(
        self, clip: TextClip, position: TextPosition
    ) -> TextClip:
        """Apply sliding animation effect."""
        duration = clip.duration
        
        if position in [TextPosition.LEFT, TextPosition.RIGHT]:
            # Horizontal slide
            w = clip.w
            if position == TextPosition.LEFT:
                start_x = lambda t: -(w + 100) * (1 - min(t, 0.5) * 2)
                clip = clip.set_position((start_x, 'center'))
            else:
                start_x = lambda t: (w + 100) * (1 - min(t, 0.5) * 2)
                clip = clip.set_position((start_x, 'center'))
        else:
            # Vertical slide
            h = clip.h
            if position == TextPosition.TOP:
                start_y = lambda t: -(h + 100) * (1 - min(t, 0.5) * 2)
                clip = clip.set_position(('center', start_y))
            else:
                start_y = lambda t: (h + 100) * (1 - min(t, 0.5) * 2)
                clip = clip.set_position(('center', start_y))
        
        return clip

    def _apply_typewriter_effect(self, clip: TextClip) -> TextClip:
        """Apply typewriter animation effect."""
        duration = clip.duration
        text = clip.text
        
        def make_frame(t):
            char_count = int(len(text) * min(t * 2, 1))
            current_text = text[:char_count]
            if not current_text:
                return np.zeros((clip.h, clip.w, 3))
            temp_clip = TextClip(
                current_text,
                font=clip.font,
                fontsize=clip.fontsize,
                color=clip.color,
                stroke_color=clip.stroke_color,
                stroke_width=clip.stroke_width,
            )
            return temp_clip.get_frame(0)
        
        return VideoClip(make_frame, duration=duration)

    def _apply_highlight_effect(self, clip: TextClip) -> TextClip:
        """Apply highlight animation effect."""
        duration = clip.duration
        
        # Create highlight background
        highlight = ColorClip(
            (clip.w + 20, clip.h + 20),
            color=(255, 255, 0)
        ).set_opacity(0.3)
        
        # Animate highlight width
        def highlight_mask(t):
            progress = min(t * 2, 1)
            mask = np.zeros((clip.h + 20, clip.w + 20))
            mask[:, :int(progress * (clip.w + 20))] = 255
            return mask
        
        highlight = highlight.set_mask(
            VideoClip(lambda t: highlight_mask(t), duration=duration)
        )
        
        return CompositeVideoClip([highlight, clip])

    def _apply_bounce_effect(self, clip: TextClip) -> TextClip:
        """Apply bouncing animation effect."""
        duration = clip.duration
        
        def bounce_pos(t):
            # Simple bounce using sine wave
            bounce = np.sin(t * 2 * np.pi * 2) * 20
            return ('center', 'center', bounce)
        
        return clip.set_position(bounce_pos)

    def _apply_wave_effect(self, clip: TextClip) -> TextClip:
        """Apply wave animation effect."""
        duration = clip.duration
        
        def wave_transform(t, x, y):
            # Create wave effect using sine
            wave = np.sin(x / 30 + t * 2 * np.pi) * 10
            return x, y + wave
        
        return clip.set_position(wave_transform)

    def _apply_glitch_effect(self, clip: TextClip) -> TextClip:
        """Apply glitch animation effect."""
        duration = clip.duration
        
        def glitch_frame(t):
            frame = clip.get_frame(t)
            if np.random.random() < 0.1:  # 10% chance of glitch
                # Random offset
                offset = np.random.randint(-10, 10)
                frame = np.roll(frame, offset, axis=1)
                # Random color channel manipulation
                channel = np.random.randint(0, 3)
                frame[:, :, channel] = np.roll(
                    frame[:, :, channel], offset * 2, axis=1
                )
            return frame
        
        return VideoClip(glitch_frame, duration=duration)

    def _apply_gradient_effect(self, clip: TextClip) -> TextClip:
        """Apply gradient color animation effect."""
        duration = clip.duration
        
        def gradient_frame(t):
            frame = clip.get_frame(t)
            # Create time-based gradient
            gradient = np.linspace(0, 1, frame.shape[1])
            gradient = gradient * np.sin(t * 2 * np.pi)
            # Apply to color channels
            frame[:, :, 0] *= gradient
            frame[:, :, 1] *= gradient[::-1]
            frame[:, :, 2] *= gradient
            return frame
        
        return VideoClip(gradient_frame, duration=duration)

    def _get_position_function(
        self,
        position: TextPosition,
        custom_position: Tuple[int, int],
        clip: TextClip,
    ):
        """Get position function based on position type."""
        if position == TextPosition.CUSTOM and custom_position:
            return custom_position
        elif position == TextPosition.CENTER:
            return ('center', 'center')
        elif position == TextPosition.TOP:
            return ('center', 50)
        elif position == TextPosition.BOTTOM:
            return ('center', -50)
        elif position == TextPosition.LEFT:
            return (50, 'center')
        elif position == TextPosition.RIGHT:
            return (-50, 'center')
        else:
            return ('center', 'center')  # Default to center

    def apply_text_overlays(
        self,
        video: VideoFileClip,
        text_configs: List[Dict]
    ) -> VideoFileClip:
        """Apply multiple text overlays to a video."""
        clips = [video]
        
        for config in text_configs:
            try:
                text_clip = self.create_text_clip(**config)
                clips.append(text_clip)
            except Exception as e:
                logger.error(f"Failed to create text overlay: {str(e)}")
                continue
        
        return CompositeVideoClip(clips)
