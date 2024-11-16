import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Video dimensions for different platforms
DIMENSIONS = {
    'youtube_shorts': (1080, 1920),  # 9:16
    'instagram_reels': (1080, 1920),  # 9:16
    'tiktok': (1080, 1920),  # 9:16
    'snapchat': (1080, 1920)  # 9:16
}

# Duration limits (in seconds)
DURATION_LIMITS = {
    'youtube_shorts': 60,
    'instagram_reels': 60,
    'tiktok': 60,
    'snapchat': 60
}

# Default paths
PATHS = {
    'output': 'output/',
    'assets': 'assets/',
    'temp': 'temp/',
    'templates': 'templates/'
}

# Create necessary directories
for path in PATHS.values():
    os.makedirs(path, exist_ok=True)

def get_config() -> Dict[str, Any]:
    """
    Get configuration dictionary.
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    return {
        'dimensions': DIMENSIONS,
        'duration_limits': DURATION_LIMITS,
        'paths': PATHS,
        'api_keys': {
            'pexels': os.getenv('PEXELS_API_KEY', ''),
            'pixabay': os.getenv('PIXABAY_API_KEY', '')
        }
    }
