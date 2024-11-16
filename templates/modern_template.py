from typing import Dict, Any, List
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from .base_template import VideoTemplate
from ..utils.text_effects import TextEffects

class ModernTemplate(VideoTemplate):
    """Modern template with smooth transitions and text animations."""
    
    def apply_template(
        self,
        clips: List[VideoFileClip],
        audio: AudioFileClip,
        text_content: Dict[str, str]
    ) -> VideoFileClip:
        """
        Apply modern template with animations.
        
        Args:
            clips (List[VideoFileClip]): Video clips
            audio (AudioFileClip): Audio track
            text_content (Dict[str, str]): Text content
            
        Returns:
            VideoFileClip: Final video
        """
        # Prepare clips with transitions
        processed_clips = []
        for i, clip in enumerate(clips):
            # Resize clip
            clip = clip.resize(width=self.width)
            
            # Add fade transition
            if i > 0:
                clip = clip.fadein(0.5)
            if i < len(clips) - 1:
                clip = clip.fadeout(0.5)
            
            processed_clips.append(clip)
        
        # Combine clips
        video = concatenate_videoclips(processed_clips)
        
        # Create title
        if 'title' in text_content:
            title = TextEffects.create_title(
                text_content['title'],
                (self.width, self.height),
                fontsize=60
            )
            title = TextEffects.animate_text(
                title,
                effect='zoom',
                duration=3.0
            ).set_duration(3.0)
            
            # Add title to beginning
            video = CompositeVideoClip([
                video,
                title.set_position('center')
            ])
        
        # Add captions
        if 'captions' in text_content:
            captions = [
                {
                    'text': cap,
                    'start': i * 3,
                    'end': (i + 1) * 3,
                    'position': 'bottom',
                    'style': {
                        'fontsize': 40,
                        'color': 'white',
                        'stroke_color': 'black',
                        'stroke_width': 2
                    }
                }
                for i, cap in enumerate(text_content['captions'])
            ]
            
            video = TextEffects.add_captions_to_video(video, captions)
        
        # Add audio
        video = video.set_audio(audio)
        
        return video
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Get default configuration for modern template.
        
        Returns:
            Dict[str, Any]: Default configuration
        """
        return {
            'dimensions': (1080, 1920),  # 9:16 aspect ratio
            'duration': 60,
            'transitions': {
                'type': 'fade',
                'duration': 0.5
            },
            'text': {
                'title_font': 'Arial-Bold',
                'caption_font': 'Arial',
                'title_size': 60,
                'caption_size': 40
            }
        }
