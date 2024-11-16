"""
File utility functions for ShortFactory.
"""
import os
import shutil
from pathlib import Path
from typing import List, Optional, Union

def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if it doesn't."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent

def clean_directory(path: Union[str, Path], exclude: Optional[List[str]] = None):
    """Clean a directory while preserving specified files/patterns."""
    path = Path(path)
    if not path.exists():
        return
    
    exclude = exclude or []
    for item in path.iterdir():
        if any(pattern in str(item) for pattern in exclude):
            continue
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

def get_file_size(path: Union[str, Path]) -> int:
    """Get file size in bytes."""
    return os.path.getsize(path)

def get_file_extension(path: Union[str, Path]) -> str:
    """Get file extension without the dot."""
    return Path(path).suffix.lstrip('.')

def is_media_file(path: Union[str, Path]) -> bool:
    """Check if file is a media file based on extension."""
    media_extensions = {
        'video': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'],
        'audio': ['mp3', 'wav', 'ogg', 'm4a', 'flac'],
        'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
    }
    ext = get_file_extension(path).lower()
    return any(ext in exts for exts in media_extensions.values())
