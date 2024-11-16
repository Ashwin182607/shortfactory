from typing import Dict, Any, List
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from .base_template import VideoTemplate
from ..utils.text_effects import TextEffects

class MinimalTemplate(VideoTemplate):
    """Clean, minimal template with simple transitions."""
    
    def apply_template(
        self,
        clips: List[VideoFileClip],
        audio: AudioFileClip,
        text_content: Dict[str, str]
    ) -> VideoFileClip:
        """
        Apply minimal template with clean design.
        """
        # Process clips
        processed_clips = []
        for clip in clips:
            # Center crop and resize
            clip = clip.resize(width=self.width)
            clip = clip.set_position('center')
            processed_clips.append(clip)
        
        # Combine clips with crossfade
        final_video = concatenate_videoclips(
            processed_clips,
            method="compose",
            transition=lambda t: min(1, max(0, 2*t))
        )
        
        # Add minimal title
        if 'title' in text_content:
            title = TextEffects.create_caption(
                text_content['title'],
                (self.width, self.height),
                fontsize=50,
                color='white',
                stroke_width=0
            )
            title = TextEffects.animate_text(
                title,
                effect='fade',
                duration=2.0
            ).set_duration(2.0)
            
            final_video = CompositeVideoClip([
                final_video,
                title.set_position(('center', 50))
            ])
        
        # Add subtle captions
        if 'captions' in text_content:
            captions = [
                {
                    'text': cap,
                    'start': i * 3,
                    'end': (i + 1) * 3,
                    'position': ('center', self.height - 80),
                    'style': {
                        'fontsize': 30,
                        'color': 'white',
                        'stroke_width': 0
                    }
                }
                for i, cap in enumerate(text_content['captions'])
            ]
            
            final_video = TextEffects.add_captions_to_video(
                final_video,
                captions
            )
        
        # Add subtle gradient overlay
        overlay = TextEffects.create_overlay(
            (self.width, self.height),
            style='gradient',
            opacity=0.2
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
        """Get default configuration for minimal template."""
        return {
            'dimensions': (1080, 1920),
            'duration': 60,
            'transitions': {
                'type': 'crossfade',
                'duration': 0.5
            },
            'text': {
                'title_font': 'Helvetica',
                'caption_font': 'Helvetica-Light',
                'title_size': 50,
                'caption_size': 30
            }
        }
