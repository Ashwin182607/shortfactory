"""
Base voice module for text-to-speech functionality.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import hashlib
import os
from typing import Optional, Dict, Any

from factory_core.database.db_base import CacheDocument
from factory_core.exceptions import (
    AudioError, VoiceGenerationError, AudioProcessingError,
    VoiceQuotaError, AudioFileError
)

class VoiceModule(ABC):
    """Base class for voice synthesis modules."""
    
    def __init__(self, cache_namespace: str):
        """Initialize voice module.
        
        Args:
            cache_namespace: Namespace for caching voice data
            
        Raises:
            AudioError: If voice module initialization fails
        """
        try:
            self.cache = CacheDocument(cache_namespace, "voice_cache")
            self.output_dir = Path("generated/audio")
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise AudioError(f"Voice module initialization failed: {str(e)}")

    def _generate_cache_key(self, text: str, voice_id: str) -> str:
        """Generate unique cache key for voice request.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier
            
        Returns:
            Cache key string
        """
        key_data = f"{text}_{voice_id}".encode('utf-8')
        return hashlib.md5(key_data).hexdigest()

    def get_cached_audio(self, text: str, voice_id: str) -> Optional[str]:
        """Retrieve cached audio file path.
        
        Args:
            text: Text that was synthesized
            voice_id: Voice identifier used
            
        Returns:
            Path to cached audio file if exists, None otherwise
            
        Raises:
            AudioFileError: If cached file exists but is invalid
        """
        try:
            cache_key = self._generate_cache_key(text, voice_id)
            cached_path = self.cache.get_if_fresh(cache_key)
            
            if cached_path and os.path.exists(cached_path):
                if os.path.getsize(cached_path) == 0:
                    raise AudioFileError(f"Cached audio file is empty: {cached_path}")
                return cached_path
            return None
        except Exception as e:
            if isinstance(e, AudioFileError):
                raise
            return None

    def cache_audio_file(self, text: str, voice_id: str, file_path: str, expiry_seconds: Optional[int] = None) -> None:
        """Cache generated audio file.
        
        Args:
            text: Text that was synthesized
            voice_id: Voice identifier used
            file_path: Path to generated audio file
            expiry_seconds: Optional cache expiry time
            
        Raises:
            AudioFileError: If file caching fails
        """
        try:
            if not os.path.exists(file_path):
                raise AudioFileError(f"Audio file does not exist: {file_path}")
                
            if os.path.getsize(file_path) == 0:
                raise AudioFileError(f"Generated audio file is empty: {file_path}")
                
            cache_key = self._generate_cache_key(text, voice_id)
            self.cache.set_with_expiry(cache_key, file_path, expiry_seconds)
            
        except Exception as e:
            if isinstance(e, AudioFileError):
                raise
            raise AudioFileError(f"Failed to cache audio file: {str(e)}")

    @abstractmethod
    def generate_voice(self, text: str, voice_id: str, output_path: Optional[str] = None) -> str:
        """Generate voice audio from text.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier to use
            output_path: Optional custom output path
            
        Returns:
            Path to generated audio file
            
        Raises:
            VoiceGenerationError: If voice generation fails
            VoiceQuotaError: If service quota is exceeded
            AudioProcessingError: If audio processing fails
        """
        pass

    def _validate_text(self, text: str) -> None:
        """Validate input text.
        
        Args:
            text: Text to validate
            
        Raises:
            ValueError: If text is invalid
        """
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
            
        if len(text) > 5000:  # Example limit
            raise ValueError("Text exceeds maximum length of 5000 characters")

    def _validate_voice_id(self, voice_id: str) -> None:
        """Validate voice identifier.
        
        Args:
            voice_id: Voice ID to validate
            
        Raises:
            ValueError: If voice ID is invalid
        """
        if not voice_id or not isinstance(voice_id, str):
            raise ValueError("Voice ID must be a non-empty string")

    def _prepare_output_path(self, text: str, voice_id: str, output_path: Optional[str] = None) -> str:
        """Prepare output path for audio file.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier
            output_path: Optional custom output path
            
        Returns:
            Prepared output path
            
        Raises:
            AudioFileError: If output path preparation fails
        """
        try:
            if output_path:
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                return output_path
                
            cache_key = self._generate_cache_key(text, voice_id)
            return str(self.output_dir / f"{cache_key}.mp3")
            
        except Exception as e:
            raise AudioFileError(f"Failed to prepare output path: {str(e)}")

    def synthesize(self, text: str, voice_id: str, output_path: Optional[str] = None,
                  use_cache: bool = True, cache_expiry: Optional[int] = None) -> str:
        """Synthesize voice with caching.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier
            output_path: Optional custom output path
            use_cache: Whether to use caching
            cache_expiry: Optional cache expiry time
            
        Returns:
            Path to audio file
            
        Raises:
            VoiceGenerationError: If voice generation fails
            AudioProcessingError: If audio processing fails
            AudioFileError: If file operations fail
        """
        try:
            self._validate_text(text)
            self._validate_voice_id(voice_id)
            
            if use_cache:
                cached_path = self.get_cached_audio(text, voice_id)
                if cached_path:
                    return cached_path
                    
            output_path = self._prepare_output_path(text, voice_id, output_path)
            
            try:
                result_path = self.generate_voice(text, voice_id, output_path)
            except Exception as e:
                if "quota exceeded" in str(e).lower():
                    raise VoiceQuotaError("Voice service quota exceeded")
                raise VoiceGenerationError(f"Voice generation failed: {str(e)}")
                
            if use_cache:
                self.cache_audio_file(text, voice_id, result_path, cache_expiry)
                
            return result_path
            
        except Exception as e:
            if isinstance(e, (VoiceGenerationError, AudioProcessingError, AudioFileError, VoiceQuotaError)):
                raise
            raise AudioProcessingError(f"Voice synthesis failed: {str(e)}")
