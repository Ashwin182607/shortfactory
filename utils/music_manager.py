import os
import json
from typing import List, Optional, Dict
import requests
from pydub import AudioSegment

class MusicManager:
    def __init__(self, api_key: str, cache_dir: str = 'assets/music/'):
        """
        Initialize music manager.
        
        Args:
            api_key (str): Pixabay API key
            cache_dir (str): Directory to cache downloaded music
        """
        self.api_key = api_key
        self.cache_dir = cache_dir
        self.base_url = "https://pixabay.com/api/"
        os.makedirs(cache_dir, exist_ok=True)
        
    def search_music(
        self,
        query: str,
        duration: Optional[int] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Search for music tracks on Pixabay.
        
        Args:
            query (str): Search query
            duration (int, optional): Desired duration in seconds
            limit (int): Maximum number of results
            
        Returns:
            List[Dict]: List of track information
        """
        params = {
            'key': self.api_key,
            'q': query,
            'media_type': 'music',
            'per_page': limit
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            hits = response.json().get('hits', [])
            
            # Filter by duration if specified
            if duration:
                hits = [
                    hit for hit in hits
                    if abs(hit.get('duration', 0) - duration) <= 10
                ]
            
            return hits[:limit]
        except Exception as e:
            print(f"Error searching music: {str(e)}")
            return []
    
    def download_track(self, track_url: str, filename: Optional[str] = None) -> Optional[str]:
        """
        Download a music track.
        
        Args:
            track_url (str): URL of the track
            filename (str, optional): Custom filename
            
        Returns:
            str: Path to downloaded file
        """
        try:
            if not filename:
                filename = f"track_{hash(track_url)}.mp3"
            
            output_path = os.path.join(self.cache_dir, filename)
            
            if os.path.exists(output_path):
                return output_path
            
            response = requests.get(track_url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return output_path
        except Exception as e:
            print(f"Error downloading track: {str(e)}")
            return None
    
    def adjust_music_duration(
        self,
        music_path: str,
        target_duration: float,
        fade_duration: float = 3.0
    ) -> str:
        """
        Adjust music duration and add fade effects.
        
        Args:
            music_path (str): Path to music file
            target_duration (float): Desired duration in seconds
            fade_duration (float): Duration of fade effects in seconds
            
        Returns:
            str: Path to adjusted music file
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(music_path)
            
            # Convert durations to milliseconds
            target_ms = target_duration * 1000
            fade_ms = fade_duration * 1000
            
            # Adjust length
            if len(audio) < target_ms:
                # Loop the audio if it's too short
                repeats = int(target_ms / len(audio)) + 1
                audio = audio * repeats
            
            # Trim to target duration
            audio = audio[:target_ms]
            
            # Add fade effects
            audio = audio.fade_in(fade_ms).fade_out(fade_ms)
            
            # Save adjusted file
            output_path = os.path.join(
                self.cache_dir,
                f"adjusted_{os.path.basename(music_path)}"
            )
            audio.export(output_path, format="mp3")
            
            return output_path
        except Exception as e:
            print(f"Error adjusting music: {str(e)}")
            return music_path  # Return original file if adjustment fails
