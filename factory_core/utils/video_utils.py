"""
Video processing utilities for ShortFactory.
"""
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Union

import cv2
import numpy as np
from moviepy.editor import VideoFileClip

logger = logging.getLogger(__name__)

def get_video_info(video_path: Union[str, Path]) -> dict:
    """
    Get video metadata.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dict containing video information
    """
    try:
        clip = VideoFileClip(str(video_path))
        return {
            'duration': clip.duration,
            'fps': clip.fps,
            'size': clip.size,
            'audio': clip.audio is not None
        }
    except Exception as e:
        logger.error(f"Error getting video info: {e}")
        return {}
    finally:
        if 'clip' in locals():
            clip.close()

def extract_frames(
    video_path: Union[str, Path],
    output_dir: Union[str, Path],
    fps: Optional[float] = None,
    max_frames: Optional[int] = None
) -> List[Path]:
    """
    Extract frames from video.
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save frames
        fps: Frames per second to extract (default: video fps)
        max_frames: Maximum number of frames to extract
        
    Returns:
        List of paths to extracted frames
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if fps is None:
        fps = video_fps
    
    frame_interval = int(video_fps / fps)
    frame_count = 0
    saved_frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            frame_path = output_dir / f"frame_{frame_count:06d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            saved_frames.append(frame_path)
            
            if max_frames and len(saved_frames) >= max_frames:
                break
                
        frame_count += 1
    
    cap.release()
    return saved_frames

def get_video_resolution(video_path: Union[str, Path]) -> Tuple[int, int]:
    """
    Get video resolution.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Tuple of (width, height)
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    
    return width, height
