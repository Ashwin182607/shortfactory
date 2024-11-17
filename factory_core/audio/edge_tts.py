"""
Edge TTS voice module implementation.
"""

import asyncio
import edge_tts
from typing import Optional, Dict, Any

from factory_core.audio.voice_base import VoiceModule
from factory_core.exceptions import (
    VoiceGenerationError, AudioProcessingError, VoiceQuotaError
)

class EdgeTTSVoice(VoiceModule):
    """Edge TTS voice implementation."""
    
    def __init__(self):
        """Initialize Edge TTS voice module.
        
        Raises:
            AudioProcessingError: If initialization fails
        """
        try:
            super().__init__("edge_tts")
            self.communicate = edge_tts.Communicate()
        except Exception as e:
            raise AudioProcessingError(f"Edge TTS initialization failed: {str(e)}")

    async def _generate_voice_async(self, text: str, voice_id: str, output_path: str) -> None:
        """Generate voice asynchronously.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier
            output_path: Output file path
            
        Raises:
            VoiceGenerationError: If voice generation fails
        """
        try:
            await self.communicate.write_to_file(
                text=text,
                voice=voice_id,
                filepath=output_path
            )
        except Exception as e:
            raise VoiceGenerationError(f"Edge TTS voice generation failed: {str(e)}")

    def generate_voice(self, text: str, voice_id: str, output_path: Optional[str] = None) -> str:
        """Generate voice using Edge TTS.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier
            output_path: Optional output path
            
        Returns:
            Path to generated audio file
            
        Raises:
            VoiceGenerationError: If voice generation fails
            AudioProcessingError: If audio processing fails
        """
        try:
            if not output_path:
                output_path = self._prepare_output_path(text, voice_id)
                
            # Run async generation in event loop
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                self._generate_voice_async(text, voice_id, output_path)
            )
            
            return output_path
            
        except Exception as e:
            if isinstance(e, VoiceGenerationError):
                raise
            raise AudioProcessingError(f"Edge TTS processing failed: {str(e)}")

    @staticmethod
    async def list_voices() -> Dict[str, Any]:
        """List available Edge TTS voices.
        
        Returns:
            Dictionary of available voices and their properties
            
        Raises:
            AudioProcessingError: If listing voices fails
        """
        try:
            voices = await edge_tts.list_voices()
            return {voice["ShortName"]: voice for voice in voices}
        except Exception as e:
            raise AudioProcessingError(f"Failed to list Edge TTS voices: {str(e)}")

    def get_voice_list(self) -> Dict[str, Any]:
        """Get list of available voices.
        
        Returns:
            Dictionary of available voices
            
        Raises:
            AudioProcessingError: If retrieving voices fails
        """
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.list_voices())
        except Exception as e:
            raise AudioProcessingError(f"Failed to get Edge TTS voice list: {str(e)}")

    def validate_voice(self, voice_id: str) -> bool:
        """Validate if voice ID exists.
        
        Args:
            voice_id: Voice identifier to validate
            
        Returns:
            True if voice exists, False otherwise
            
        Raises:
            AudioProcessingError: If voice validation fails
        """
        try:
            voices = self.get_voice_list()
            return voice_id in voices
        except Exception as e:
            raise AudioProcessingError(f"Voice validation failed: {str(e)}")

    def get_voice_properties(self, voice_id: str) -> Optional[Dict[str, Any]]:
        """Get properties for a specific voice.
        
        Args:
            voice_id: Voice identifier
            
        Returns:
            Voice properties if voice exists, None otherwise
            
        Raises:
            AudioProcessingError: If retrieving properties fails
        """
        try:
            voices = self.get_voice_list()
            return voices.get(voice_id)
        except Exception as e:
            raise AudioProcessingError(f"Failed to get voice properties: {str(e)}")

    def get_voice_by_language(self, language_code: str) -> Optional[str]:
        """Get first available voice for a language.
        
        Args:
            language_code: Language code (e.g., 'en-US')
            
        Returns:
            Voice ID if found, None otherwise
            
        Raises:
            AudioProcessingError: If voice search fails
        """
        try:
            voices = self.get_voice_list()
            for voice_id, props in voices.items():
                if props["Locale"].lower() == language_code.lower():
                    return voice_id
            return None
        except Exception as e:
            raise AudioProcessingError(f"Failed to find voice for language {language_code}: {str(e)}")

    def get_supported_languages(self) -> Dict[str, int]:
        """Get dictionary of supported languages and voice count.
        
        Returns:
            Dictionary mapping language codes to number of available voices
            
        Raises:
            AudioProcessingError: If getting languages fails
        """
        try:
            voices = self.get_voice_list()
            languages = {}
            for props in voices.values():
                locale = props["Locale"]
                languages[locale] = languages.get(locale, 0) + 1
            return languages
        except Exception as e:
            raise AudioProcessingError(f"Failed to get supported languages: {str(e)}")

    def get_voices_for_language(self, language_code: str) -> Dict[str, Any]:
        """Get all voices for a specific language.
        
        Args:
            language_code: Language code (e.g., 'en-US')
            
        Returns:
            Dictionary of voice IDs and properties for the language
            
        Raises:
            AudioProcessingError: If getting voices fails
        """
        try:
            voices = self.get_voice_list()
            return {
                voice_id: props 
                for voice_id, props in voices.items()
                if props["Locale"].lower() == language_code.lower()
            }
        except Exception as e:
            raise AudioProcessingError(f"Failed to get voices for language {language_code}: {str(e)}")
