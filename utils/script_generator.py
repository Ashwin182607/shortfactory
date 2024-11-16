from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import os
from typing import Dict, Any, Optional

class ScriptGenerator:
    def __init__(self, model_name: str = "EleutherAI/gpt-neo-125M"):
        """
        Initialize the script generator with a specified model.
        Using GPT-Neo 125M as default (smaller, free alternative to GPT-J).
        
        Args:
            model_name (str): Name of the HuggingFace model to use
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.generator = pipeline(
            'text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
            device=-1  # Use CPU
        )
        
    def generate_script(
        self,
        prompt: str,
        max_length: int = 200,
        platform: str = "youtube_shorts"
    ) -> Dict[str, Any]:
        """
        Generate a script for a short video.
        
        Args:
            prompt (str): Topic or idea for the video
            max_length (int): Maximum length of the generated script
            platform (str): Target platform for optimization
            
        Returns:
            Dict[str, Any]: Dictionary containing script sections
        """
        # Create platform-specific prompt
        platform_prompts = {
            "youtube_shorts": "Create a 60-second YouTube Shorts script about:",
            "instagram_reels": "Write an engaging Instagram Reels script about:",
            "tiktok": "Write a viral TikTok script about:",
            "snapchat": "Create a quick Snapchat story script about:"
        }
        
        base_prompt = platform_prompts.get(platform, platform_prompts["youtube_shorts"])
        full_prompt = f"{base_prompt} {prompt}\n\nScript:\n"
        
        # Generate the script
        result = self.generator(
            full_prompt,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )[0]['generated_text']
        
        # Process the generated text into sections
        script_text = result.split("Script:\n")[-1].strip()
        
        # Split into sections (simple version)
        sections = script_text.split("\n\n")
        
        return {
            "intro": sections[0] if sections else "",
            "main_content": sections[1] if len(sections) > 1 else "",
            "outro": sections[2] if len(sections) > 2 else "",
            "full_script": script_text
        }
        
    @staticmethod
    def format_script_for_tts(script: Dict[str, Any]) -> str:
        """
        Format the script for text-to-speech.
        
        Args:
            script (Dict[str, Any]): Script dictionary
            
        Returns:
            str: Formatted script text
        """
        return " ".join([
            script["intro"],
            script["main_content"],
            script["outro"]
        ]).strip()
