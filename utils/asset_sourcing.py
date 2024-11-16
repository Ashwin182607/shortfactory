import os
import requests
from typing import List, Optional
from urllib.parse import urlparse

class AssetDownloader:
    def __init__(self, output_dir: str = 'assets/'):
        """
        Initialize the asset downloader.
        
        Args:
            output_dir (str): Directory to save downloaded assets
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def download_file(self, url: str, filename: Optional[str] = None) -> Optional[str]:
        """
        Download a file from a URL.
        
        Args:
            url (str): URL of the file to download
            filename (str, optional): Custom filename. If None, extracts from URL
            
        Returns:
            str: Path to the downloaded file
        """
        try:
            if not filename:
                filename = os.path.basename(urlparse(url).path)
                if not filename:
                    filename = 'asset_' + str(hash(url))[:8]
            
            output_path = os.path.join(self.output_dir, filename)
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return output_path
        except Exception as e:
            print(f"Error downloading asset: {str(e)}")
            return None

class PexelsDownloader(AssetDownloader):
    def __init__(self, api_key: str, output_dir: str = 'assets/'):
        """
        Initialize Pexels downloader.
        
        Args:
            api_key (str): Pexels API key
            output_dir (str): Directory to save downloaded assets
        """
        super().__init__(output_dir)
        self.api_key = api_key
        self.headers = {'Authorization': api_key}
        self.base_url = 'https://api.pexels.com/v1'
        
    def search_videos(self, query: str, per_page: int = 5) -> List[str]:
        """
        Search for videos on Pexels.
        
        Args:
            query (str): Search query
            per_page (int): Number of results to return
            
        Returns:
            List[str]: List of video URLs
        """
        try:
            response = requests.get(
                f"{self.base_url}/videos/search",
                headers=self.headers,
                params={'query': query, 'per_page': per_page}
            )
            response.raise_for_status()
            
            videos = response.json().get('videos', [])
            return [v['video_files'][0]['link'] for v in videos if v['video_files']]
        except Exception as e:
            print(f"Error searching Pexels videos: {str(e)}")
            return []
    
    def download_videos(self, query: str, count: int = 5) -> List[str]:
        """
        Search and download videos from Pexels.
        
        Args:
            query (str): Search query
            count (int): Number of videos to download
            
        Returns:
            List[str]: Paths to downloaded videos
        """
        video_urls = self.search_videos(query, count)
        downloaded = []
        
        for i, url in enumerate(video_urls):
            filename = f"{query.replace(' ', '_')}_{i}.mp4"
            path = self.download_file(url, filename)
            if path:
                downloaded.append(path)
                
        return downloaded
