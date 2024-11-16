from typing import Dict, List, Optional
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
import json
import os
import logging

logger = logging.getLogger(__name__)

class ScriptGenerator:
    """AI-powered script generation using Hugging Face models."""
    
    def __init__(self, model_name: str = "EleutherAI/gpt-neo-125M"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(self.device)
        
        # Load prompt templates
        self.load_templates()
    
    def load_templates(self):
        """Load prompt templates for different platforms."""
        self.templates = {
            "YouTube Shorts": {
                "intro": "Create an attention-grabbing introduction for a YouTube Short about {topic}. Keep it under 15 seconds.",
                "main": "Write the main content for a YouTube Short about {topic}. Focus on key points and keep it engaging.",
                "outro": "Create a strong call-to-action outro for this YouTube Short about {topic}."
            },
            "Instagram Reels": {
                "intro": "Write a trendy, engaging intro for an Instagram Reel about {topic}. Make it catchy and relatable.",
                "main": "Create the main content for an Instagram Reel about {topic}. Keep it dynamic and visually descriptive.",
                "outro": "Write a memorable outro for this Instagram Reel about {topic} with a clear call-to-action."
            },
            "TikTok": {
                "intro": "Create a hook for a TikTok video about {topic}. Make it impossible to scroll past.",
                "main": "Write the main content for a TikTok about {topic}. Keep it fast-paced and entertaining.",
                "outro": "Create a viral-worthy outro for this TikTok about {topic}."
            }
        }
    
    def generate_section(
        self,
        template: str,
        topic: str,
        max_length: int = 100,
        temperature: float = 0.7
    ) -> str:
        """Generate a specific section of the script."""
        prompt = template.format(topic=topic)
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Generate text
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            temperature=temperature,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Decode and clean up the generated text
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text.replace(prompt, "").strip()
    
    def generate_script(
        self,
        topic: str,
        platform: str = "YouTube Shorts",
        style: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate a complete video script."""
        if platform not in self.templates:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Get platform-specific templates
        templates = self.templates[platform]
        
        # Generate each section
        script = {
            "intro": self.generate_section(templates["intro"], topic, max_length=50),
            "main": self.generate_section(templates["main"], topic, max_length=200),
            "outro": self.generate_section(templates["outro"], topic, max_length=50)
        }
        
        return script
    
    def estimate_duration(self, script: Dict[str, str]) -> float:
        """Estimate video duration based on script length."""
        # Rough estimate: 2.5 words per second for natural speech
        total_words = sum(len(section.split()) for section in script.values())
        return total_words / 2.5
    
    def get_keywords(self, script: Dict[str, str], num_keywords: int = 5) -> List[str]:
        """Extract keywords from the script for asset searching."""
        # Combine all script sections
        full_text = " ".join(script.values())
        
        # Use text classification pipeline for keyword extraction
        classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Candidate labels for classification
        candidate_labels = [
            "nature", "technology", "business", "lifestyle", "sports",
            "food", "travel", "education", "entertainment", "health",
            "fashion", "music", "art", "science", "gaming"
        ]
        
        # Get classification results
        result = classifier(full_text, candidate_labels)
        
        # Return top keywords based on scores
        sorted_keywords = [label for _, label in sorted(
            zip(result['scores'], result['labels']),
            reverse=True
        )]
        
        return sorted_keywords[:num_keywords]
    
    @staticmethod
    def format_script(script: Dict[str, str]) -> str:
        """Format the script for display."""
        return "\n\n".join([
            f"[INTRO]\n{script['intro']}",
            f"[MAIN CONTENT]\n{script['main']}",
            f"[OUTRO]\n{script['outro']}"
        ])
