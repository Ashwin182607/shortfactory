from gtts import gTTS
import os
from typing import Optional

def generate_speech(
    text: str,
    output_path: str,
    language: str = 'en',
    slow: bool = False
) -> str:
    """
    Generate speech from text using Google Text-to-Speech.
    
    Args:
        text (str): Text to convert to speech
        output_path (str): Path to save the audio file
        language (str, optional): Language code. Defaults to 'en'.
        slow (bool, optional): Whether to speak slowly. Defaults to False.
        
    Returns:
        str: Path to the generated audio file
    """
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=slow)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save audio file
        tts.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"Error generating speech: {str(e)}")
        return None
