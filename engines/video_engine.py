from typing import List, Tuple, Optional
import os
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip
from ..utils.tts import generate_speech
from ..utils.asset_sourcing import PexelsDownloader
from ..utils.music_manager import MusicManager
from ..utils.script_generator import ScriptGenerator
from ..utils.text_effects import TextEffects
from ..templates.modern_template import ModernTemplate
from .base_engine import BaseEngine

class VideoEngine(BaseEngine):
    def __init__(self, config):
        """
        Initialize video engine with configuration.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.pexels = PexelsDownloader(
            api_key=config['api_keys']['pexels'],
            output_dir=config['paths']['assets']
        )
        self.music = MusicManager(
            api_key=config['api_keys']['pixabay'],
            cache_dir=os.path.join(config['paths']['assets'], 'music')
        )
        self.script_gen = ScriptGenerator()
        self.dimensions = config['dimensions']
        self.duration_limits = config['duration_limits']
        self.template = ModernTemplate(ModernTemplate.get_default_config())
        
    def generate_script(self, prompt: str) -> str:
        """
        Generate video script from prompt using AI.
        
        Args:
            prompt (str): Video topic/idea
            
        Returns:
            str: Generated script
        """
        script_data = self.script_gen.generate_script(prompt)
        return self.script_gen.format_script_for_tts(script_data)
    
    def source_assets(self, script: str) -> List[str]:
        """
        Source video assets based on script.
        
        Args:
            script (str): Video script
            
        Returns:
            List[str]: List of asset file paths
        """
        # Get videos from Pexels
        videos = self.pexels.download_videos(script, count=3)
        
        # Get background music
        music_tracks = self.music.search_music("upbeat background", duration=60)
        if music_tracks:
            music_path = self.music.download_track(music_tracks[0]['audio'])
            if music_path:
                videos.append(music_path)
        
        return videos
    
    def generate_voiceover(self, script: str) -> str:
        """
        Generate voiceover from script.
        
        Args:
            script (str): Video script
            
        Returns:
            str: Path to voiceover audio file
        """
        output_path = os.path.join(self.config['paths']['temp'], 'voiceover.mp3')
        return generate_speech(script, output_path)
    
    def edit_video(self, assets: List[str], voiceover: str, output_path: str) -> str:
        """
        Edit and render final video.
        
        Args:
            assets (List[str]): List of asset file paths
            voiceover (str): Path to voiceover audio file
            output_path (str): Output video path
            
        Returns:
            str: Path to output video
        """
        try:
            # Separate video assets and music
            video_assets = [a for a in assets if not a.endswith('.mp3')]
            music_assets = [a for a in assets if a.endswith('.mp3')]
            
            # Load video clips
            video_clips = [VideoFileClip(asset) for asset in video_assets]
            
            # Load audio
            voiceover_audio = AudioFileClip(voiceover)
            
            # Load and adjust background music if available
            if music_assets:
                music_audio = AudioFileClip(music_assets[0])
                music_audio = self.music.adjust_music_duration(
                    music_assets[0],
                    voiceover_audio.duration
                )
                # Mix voiceover and music
                final_audio = CompositeAudioClip([
                    voiceover_audio,
                    AudioFileClip(music_audio).volumex(0.3)
                ])
            else:
                final_audio = voiceover_audio
            
            # Prepare text content
            text_content = {
                'title': 'Your Video Title',  # This should come from script
                'captions': [
                    'Caption 1',  # These should be generated from script
                    'Caption 2',
                    'Caption 3'
                ]
            }
            
            # Apply template
            final_video = self.template.apply_template(
                video_clips,
                final_audio,
                text_content
            )
            
            # Write output file
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Clean up
            final_video.close()
            for clip in video_clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error editing video: {str(e)}")
            return None
