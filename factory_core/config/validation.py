"""
Configuration validation utilities.
"""
from typing import Dict, List, Optional, Union
import os
from pathlib import Path
import logging
import importlib
import torch

from rich.console import Console
from rich.table import Table

logger = logging.getLogger(__name__)
console = Console()

class ConfigValidator:
    """Validates ShortFactory configuration."""
    
    @staticmethod
    def validate_api_keys() -> Dict[str, bool]:
        """Validate required API keys."""
        keys = {
            "PEXELS_API_KEY": os.getenv("PEXELS_API_KEY"),
            "PIXABAY_API_KEY": os.getenv("PIXABAY_API_KEY"),
            "UNSPLASH_API_KEY": os.getenv("UNSPLASH_API_KEY"),
        }
        return {k: bool(v) for k, v in keys.items()}
    
    @staticmethod
    def validate_directories() -> Dict[str, bool]:
        """Validate required directories."""
        dirs = {
            "assets": Path("assets"),
            "models": Path("models"),
            "cache": Path(".cache"),
            "output": Path("output"),
            "logs": Path("logs"),
        }
        
        status = {}
        for name, path in dirs.items():
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    status[name] = True
                except Exception as e:
                    logger.error(f"Failed to create {name} directory: {e}")
                    status[name] = False
            else:
                status[name] = True
        return status
    
    @staticmethod
    def validate_dependencies() -> Dict[str, bool]:
        """Validate required Python dependencies."""
        dependencies = {
            # Core
            "torch": "PyTorch",
            "transformers": "Transformers",
            "gradio": "Gradio",
            "moviepy": "MoviePy",
            
            # Image Processing
            "PIL": "Pillow",
            "cv2": "OpenCV",
            "numpy": "NumPy",
            
            # Audio Processing
            "soundfile": "SoundFile",
            "librosa": "Librosa",
            
            # Text Processing
            "nltk": "NLTK",
            "spacy": "spaCy",
            
            # Utilities
            "tqdm": "TQDM",
            "requests": "Requests",
            "diskcache": "DiskCache",
            "tenacity": "Tenacity",
            "yaml": "PyYAML",
        }
        
        status = {}
        for module_name, display_name in dependencies.items():
            try:
                importlib.import_module(module_name)
                status[display_name] = True
            except ImportError:
                status[display_name] = False
        return status
    
    @staticmethod
    def validate_gpu() -> Dict[str, Union[bool, str]]:
        """Validate GPU availability and CUDA version."""
        status = {
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": None,
            "device_count": 0,
            "device_names": [],
        }
        
        if status["cuda_available"]:
            status["cuda_version"] = torch.version.cuda
            status["device_count"] = torch.cuda.device_count()
            status["device_names"] = [
                torch.cuda.get_device_name(i)
                for i in range(status["device_count"])
            ]
        
        return status
    
    def validate_all(self) -> Dict[str, Dict]:
        """Run all validation checks."""
        results = {
            "API Keys": self.validate_api_keys(),
            "Directories": self.validate_directories(),
            "Dependencies": self.validate_dependencies(),
            "GPU": self.validate_gpu(),
        }
        
        # Create summary table
        table = Table(title="ShortFactory Configuration Validation")
        table.add_column("Category", style="cyan")
        table.add_column("Item", style="magenta")
        table.add_column("Status", style="green")
        
        for category, items in results.items():
            for item, status in items.items():
                status_symbol = "[green]✓[/green]" if status else "[red]✗[/red]"
                table.add_row(category, str(item), status_symbol)
        
        console.print(table)
        return results
