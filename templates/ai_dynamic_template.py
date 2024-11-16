from typing import Dict, List, Any
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from utils.text_effects import TextEffects
from templates.base_template import VideoTemplate
import numpy as np
import time

class AIDynamicTemplate(VideoTemplate):
    """Dynamic template with AI-powered transitions and effects."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize template with configuration."""
        super().__init__(config)
        self.text_effects = TextEffects()
        self.transition_duration = config.get('transition_duration', 0.5)
        self.text_duration = config.get('text_duration', 3.0)
        self.style = config.get('style', 'modern')
        
    def create_section(
        self,
        clip: VideoFileClip,
        text: str,
        position: str = 'bottom',
        effect: str = 'fade'
    ) -> CompositeVideoClip:
        """Create a section with text overlay and effects."""
        # Create text overlay
        if position == 'center':
            txt_clip = self.text_effects.create_title(
                text,
                clip.size,
                fontsize=60,
                bg_opacity=0.6
            )
        else:
            txt_clip = self.text_effects.create_caption(
                text,
                clip.size,
                fontsize=40
            )
        
        # Apply animation effect
        txt_clip = self.text_effects.animate_text(
            txt_clip,
            effect=effect,
            duration=self.text_duration
        )
        
        # Set position
        if position == 'top':
            txt_clip = txt_clip.set_position(('center', 50))
        elif position == 'bottom':
            txt_clip = txt_clip.set_position(('center', clip.h - 100))
        else:  # center
            txt_clip = txt_clip.set_position('center')
        
        # Add overlay
        overlay = self.text_effects.create_overlay(
            clip.size,
            style='gradient' if self.style == 'modern' else 'vignette',
            opacity=0.2
        )
        
        return CompositeVideoClip([clip, overlay, txt_clip])
    
    def apply_ai_transition(
        self,
        clip1: VideoFileClip,
        clip2: VideoFileClip
    ) -> VideoFileClip:
        """Apply AI-powered transition effect."""
        # Create transition using a dynamic mask
        def transition_mask(t):
            """Generate dynamic transition mask."""
            progress = t / self.transition_duration
            if self.style == 'modern':
                # Modern slide effect
                return np.tile(
                    np.array([1 if x < progress else 0
                             for x in np.linspace(0, 1, clip1.w)]),
                    (clip1.h, 1)
                )
            else:
                # Circular reveal effect
                x = np.linspace(-1, 1, clip1.w)
                y = np.linspace(-1, 1, clip1.h)
                X, Y = np.meshgrid(x, y)
                R = np.sqrt(X**2 + Y**2)
                return R > (1.5 * (1 - progress))
        
        # Create transition clip
        transition = CompositeVideoClip([
            clip1.set_end(self.transition_duration),
            clip2.set_start(0).set_end(self.transition_duration)
        ])
        
        # Apply mask
        transition = transition.set_mask(
            lambda t: transition_mask(t)
        )
        
        return concatenate_videoclips([
            clip1.set_end(clip1.duration - self.transition_duration),
            transition,
            clip2.set_start(self.transition_duration)
        ])
    
    def apply_template(
        self,
        clips: List[VideoFileClip],
        audio: AudioFileClip,
        text_content: Dict[str, str]
    ) -> VideoFileClip:
        """Apply template to video clips."""
        # Process intro
        intro = self.create_section(
            clips[0],
            text_content['intro'],
            position='center',
            effect='zoom'
        )
        
        # Process main content
        main_clips = []
        main_sentences = text_content['main'].split('. ')
        for i, (clip, text) in enumerate(zip(clips[1:-1], main_sentences)):
            section = self.create_section(
                clip,
                text,
                position='bottom',
                effect=['fade', 'slide', 'typewriter'][i % 3]
            )
            main_clips.append(section)
        
        # Process outro
        outro = self.create_section(
            clips[-1],
            text_content['outro'],
            position='center',
            effect='split'
        )
        
        # Combine clips with AI transitions
        final_clips = [intro]
        for clip in main_clips:
            if len(final_clips) > 0:
                # Apply AI transition between clips
                combined = self.apply_ai_transition(
                    final_clips[-1],
                    clip
                )
                final_clips[-1] = combined
            else:
                final_clips.append(clip)
        
        # Add outro with transition
        if len(final_clips) > 0:
            final_clips.append(
                self.apply_ai_transition(final_clips[-1], outro)
            )
        else:
            final_clips.append(outro)
        
        # Combine all clips
        final_video = concatenate_videoclips(final_clips)
        
        # Add audio
        final_video = final_video.set_audio(audio)
        
        return final_video
