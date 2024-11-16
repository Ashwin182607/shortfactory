from typing import Dict, Any, List
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from .base_template import VideoTemplate
from ..utils.text_effects import TextEffects
import numpy as np

class DynamicTemplate(VideoTemplate):
    """Energetic template with dynamic transitions and effects."""
    
    def apply_template(
        self,
        clips: List[VideoFileClip],
        audio: AudioFileClip,
        text_content: Dict[str, str]
    ) -> VideoFileClip:
        """
        Apply dynamic template with energetic effects.
        """
        # Process clips with dynamic effects
        processed_clips = []
        for i, clip in enumerate(clips):
            # Resize and add motion
            clip = clip.resize(width=self.width * 1.1)  # Slightly larger for motion
            clip = clip.set_position(
                lambda t: ('center', 50 + 20 * np.sin(t * 2 * np.pi / clip.duration))
            )
            
            # Add zoom effect
            clip = clip.resize(
                lambda t: 1 + 0.1 * np.sin(t * np.pi / clip.duration)
            )
            
            # Add rotation for some clips
            if i % 2 == 0:
                clip = clip.rotate(
                    lambda t: 5 * np.sin(t * 2 * np.pi / clip.duration)
                )
            
            processed_clips.append(clip)
        
        # Combine clips with dynamic transitions
        final_video = concatenate_videoclips(
            processed_clips,
            method="compose",
            transition=lambda t: abs(np.sin(np.pi * t))
        )
        
        # Add dynamic title
        if 'title' in text_content:
            title = TextEffects.create_caption(
                text_content['title'],
                (self.width, self.height),
                fontsize=60,
                color='white',
                stroke_width=3
            )
            title = TextEffects.animate_text(
                title,
                effect='wave',
                duration=3.0
            ).set_duration(3.0)
            
            final_video = CompositeVideoClip([
                final_video,
                title.set_position(('center', 100))
            ])
        
        # Add animated captions
        if 'captions' in text_content:
            captions = []
            for i, cap in enumerate(text_content['captions']):
                caption = {
                    'text': cap,
                    'start': i * 3,
                    'end': (i + 1) * 3,
                    'position': ('center', self.height - 150),
                    'style': {
                        'fontsize': 40,
                        'color': 'white',
                        'stroke_width': 2
                    }
                }
                
                # Alternate between different animation effects
                effects = ['bounce', 'split', 'glitch', 'rotate']
                caption_clip = TextEffects.create_caption(
                    cap,
                    (self.width, self.height),
                    **caption['style']
                )
                caption_clip = TextEffects.animate_text(
                    caption_clip,
                    effect=effects[i % len(effects)],
                    duration=3.0
                )
                caption_clip = caption_clip.set_start(caption['start']).set_end(caption['end'])
                caption_clip = caption_clip.set_position(caption['position'])
                
                captions.append(caption_clip)
            
            final_video = CompositeVideoClip([final_video] + captions)
        
        # Add dynamic overlay
        overlay = TextEffects.create_overlay(
            (self.width, self.height),
            style='vignette',
            opacity=0.3
        )
        
        final_video = CompositeVideoClip([
            final_video,
            overlay
        ])
        
        # Add audio
        final_video = final_video.set_audio(audio)
        
        return final_video
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration for dynamic template."""
        return {
            'dimensions': (1080, 1920),
            'duration': 60,
            'transitions': {
                'type': 'dynamic',
                'duration': 0.7
            },
            'text': {
                'title_font': 'Impact',
                'caption_font': 'Arial-Bold',
                'title_size': 60,
                'caption_size': 40
            },
            'effects': {
                'zoom_range': 0.1,
                'rotation_range': 5,
                'motion_range': 20
            }
        }
