"""
Configuration validation utilities.
"""
from typing import Dict, List, Optional, Union
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

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
            "output": Path("output")
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
            "torch": "torch",
            "transformers": "transformers",
            "moviepy": "moviepy",
            "gradio": "gradio",
            "python-dotenv": "dotenv"
        }
        
        status = {}
        for name, module in dependencies.items():
            try:
                __import__(module)
                status[name] = True
            except ImportError:
                logger.error(f"Missing required dependency: {name}")
                status[name] = False
        return status
    
    @staticmethod
    def validate_gpu() -> Dict[str, Union[bool, str]]:
        """Validate GPU availability and CUDA version."""
        try:
            import torch
            cuda_available = torch.cuda.is_available()
            cuda_version = torch.version.cuda if cuda_available else None
            device_count = torch.cuda.device_count() if cuda_available else 0
            
            return {
                "cuda_available": cuda_available,
                "cuda_version": cuda_version,
                "device_count": device_count,
                "device_names": [torch.cuda.get_device_name(i) for i in range(device_count)] if device_count > 0 else []
            }
        except Exception as e:
            logger.error(f"Error checking GPU status: {e}")
            return {
                "cuda_available": False,
                "cuda_version": None,
                "device_count": 0,
                "device_names": []
            }
    
    @classmethod
    def validate_all(cls) -> Dict[str, Dict]:
        """Run all validation checks."""
        return {
            "api_keys": cls.validate_api_keys(),
            "directories": cls.validate_directories(),
            "dependencies": cls.validate_dependencies(),
            "gpu": cls.validate_gpu()
        }
    
    @classmethod
    def print_validation_report(cls):
        """Print a formatted validation report."""
        results = cls.validate_all()
        
        print("\n=== ShortFactory Validation Report ===\n")
        
        # API Keys
        print("API Keys:")
        for key, valid in results["api_keys"].items():
            status = "✓" if valid else "✗"
            print(f"  {status} {key}")
        
        # Directories
        print("\nDirectories:")
        for dir_name, valid in results["directories"].items():
            status = "✓" if valid else "✗"
            print(f"  {status} {dir_name}")
        
        # Dependencies
        print("\nDependencies:")
        for dep_name, valid in results["dependencies"].items():
            status = "✓" if valid else "✗"
            print(f"  {status} {dep_name}")
        
        # GPU Status
        print("\nGPU Status:")
        gpu = results["gpu"]
        if gpu["cuda_available"]:
            print(f"  ✓ CUDA {gpu['cuda_version']}")
            print(f"  ✓ {gpu['device_count']} device(s) available")
            for device in gpu["device_names"]:
                print(f"    - {device}")
        else:
            print("  ✗ No GPU available")
        
        print("\n=== End Report ===\n")
