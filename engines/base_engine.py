from abc import ABC, abstractmethod
from typing import Dict, Any, List
import os

class BaseEngine(ABC):
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the base engine with configuration.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary containing settings
        """
        self.config = config
        self.output_path = config.get('output_path', 'output/')
        os.makedirs(self.output_path, exist_ok=True)
        
    @abstractmethod
    def generate_script(self, prompt: str) -> str:
        """Generate content script from prompt."""
        pass
    
    @abstractmethod
    def source_assets(self, script: str) -> List[str]:
        """Source necessary media assets for the content."""
        pass
    
    @abstractmethod
    def generate_voiceover(self, script: str) -> str:
        """Generate voiceover from script."""
        pass
    
    @abstractmethod
    def edit_video(self, assets: List[str], voiceover: str, output_path: str) -> str:
        """Edit and render the final video."""
        pass
    
    def create_content(self, prompt: str) -> str:
        """
        Create content from prompt to final video.
        
        Args:
            prompt (str): Content prompt/idea
            
        Returns:
            str: Path to the generated video
        """
        script = self.generate_script(prompt)
        assets = self.source_assets(script)
        voiceover = self.generate_voiceover(script)
        
        output_file = os.path.join(
            self.output_path, 
            f"{prompt[:30].replace(' ', '_')}.mp4"
        )
        
        return self.edit_video(assets, voiceover, output_file)
