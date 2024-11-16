"""
Audio processing utilities for ShortFactory.
"""
import logging
from pathlib import Path
from typing import Optional, Union

import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

logger = logging.getLogger(__name__)

def get_audio_duration(audio_path: Union[str, Path]) -> float:
    """
    Get audio duration in seconds.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Duration in seconds
    """
    try:
        audio = AudioSegment.from_file(str(audio_path))
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except Exception as e:
        logger.error(f"Error getting audio duration: {e}")
        return 0.0

def trim_silence(
    audio_path: Union[str, Path],
    output_path: Union[str, Path],
    min_silence_len: int = 500,  # ms
    silence_thresh: int = -40,  # dB
    keep_silence: int = 100  # ms
) -> Optional[Path]:
    """
    Trim silence from beginning and end of audio file.
    
    Args:
        audio_path: Path to input audio file
        output_path: Path to save trimmed audio
        min_silence_len: Minimum length of silence (in ms)
        silence_thresh: Silence threshold in dB
        keep_silence: Amount of silence to keep (in ms)
        
    Returns:
        Path to trimmed audio file, or None if failed
    """
    try:
        audio = AudioSegment.from_file(str(audio_path))
        
        # Find non-silent chunks
        nonsilent_ranges = detect_nonsilent(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,
            seek_step=1
        )
        
        if not nonsilent_ranges:
            logger.warning("No non-silent ranges found")
            return None
            
        start_trim = nonsilent_ranges[0][0]
        end_trim = nonsilent_ranges[-1][1]
        
        # Keep some silence at beginning and end
        start_trim = max(0, start_trim - keep_silence)
        end_trim = min(len(audio), end_trim + keep_silence)
        
        trimmed_audio = audio[start_trim:end_trim]
        trimmed_audio.export(str(output_path), format=Path(output_path).suffix.lstrip('.'))
        
        return Path(output_path)
        
    except Exception as e:
        logger.error(f"Error trimming silence: {e}")
        return None

def normalize_audio(
    audio_path: Union[str, Path],
    output_path: Union[str, Path],
    target_db: float = -20.0
) -> Optional[Path]:
    """
    Normalize audio volume.
    
    Args:
        audio_path: Path to input audio file
        output_path: Path to save normalized audio
        target_db: Target dB level
        
    Returns:
        Path to normalized audio file, or None if failed
    """
    try:
        audio = AudioSegment.from_file(str(audio_path))
        
        # Calculate current dB level
        current_db = audio.dBFS
        
        # Calculate required gain
        gain = target_db - current_db
        
        # Apply gain
        normalized = audio.apply_gain(gain)
        
        # Export
        normalized.export(str(output_path), format=Path(output_path).suffix.lstrip('.'))
        
        return Path(output_path)
        
    except Exception as e:
        logger.error(f"Error normalizing audio: {e}")
        return None
