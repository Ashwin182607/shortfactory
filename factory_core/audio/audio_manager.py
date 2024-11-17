"""
Audio Manager for handling text-to-speech and audio processing.
"""
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

try:
    import torch
    from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    logging.warning("Speech modules not found. TTS will be disabled.")

try:
    import librosa
    import soundfile as sf
    AUDIO_PROCESSING_AVAILABLE = True
except ImportError:
    AUDIO_PROCESSING_AVAILABLE = False
    logging.warning("Audio processing modules not found. Audio effects will be limited.")

logger = logging.getLogger(__name__)

class AudioManager:
    """Manages text-to-speech and audio processing."""
    
    def __init__(self):
        """Initialize audio processing components."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models_dir = Path(__file__).parent.parent.parent / "models"
        self.cache_dir = Path(__file__).parent.parent.parent / ".cache/audio"
        
        # Create directories
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Initialize TTS if available
        if SPEECH_AVAILABLE:
            self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
            self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(self.device)
            self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(self.device)
            logger.info("TTS models loaded successfully")
    
    def generate_speech(
        self,
        text: str,
        output_path: Optional[Path] = None,
        voice_preset: str = "default",
        speaking_rate: float = 1.0
    ) -> Path:
        """Generate speech from text."""
        if not SPEECH_AVAILABLE:
            raise RuntimeError("Speech generation is not available. Please install required packages.")
        
        # Process text
        inputs = self.processor(text=text, return_tensors="pt").to(self.device)
        
        # Generate speech
        speech = self.model.generate_speech(
            inputs["input_ids"],
            self.vocoder,
            speaking_rate=speaking_rate
        )
        
        # Save audio
        if output_path is None:
            output_path = self.cache_dir / f"{hash(text)}.wav"
        
        sf.write(str(output_path), speech.cpu().numpy(), samplerate=16000)
        return output_path
    
    def process_audio(
        self,
        audio_path: Path,
        output_path: Optional[Path] = None,
        effects: Optional[Dict] = None
    ) -> Path:
        """Apply audio processing effects."""
        if not AUDIO_PROCESSING_AVAILABLE:
            raise RuntimeError("Audio processing is not available. Please install required packages.")
        
        # Load audio
        y, sr = librosa.load(str(audio_path))
        
        if effects:
            # Apply effects
            if effects.get("tempo"):
                y = librosa.effects.time_stretch(y, rate=effects["tempo"])
            
            if effects.get("pitch"):
                y = librosa.effects.pitch_shift(y, sr=sr, n_steps=effects["pitch"])
            
            if effects.get("normalize"):
                y = librosa.util.normalize(y)
        
        # Save processed audio
        if output_path is None:
            output_path = self.cache_dir / f"processed_{audio_path.name}"
        
        sf.write(str(output_path), y, sr)
        return output_path
    
    def clear_cache(self):
        """Clear audio cache."""
        if os.path.exists(self.cache_dir):
            for file in os.listdir(self.cache_dir):
                os.remove(self.cache_dir / file)
            logger.info("Audio cache cleared")
