"""
Configuration management for ShortFactory.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file, defaults to config.yaml in project root
        
    Returns:
        Dict containing configuration
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / 'config.yaml'
    
    if not config_path.exists():
        return {}
        
    with open(config_path) as f:
        return yaml.safe_load(f)

def load_env(env_path: Optional[Path] = None) -> None:
    """
    Load environment variables from .env file.
    
    Args:
        env_path: Path to .env file, defaults to .env in project root
    """
    if env_path is None:
        env_path = Path(__file__).parent.parent.parent / '.env'
    
    if env_path.exists():
        load_dotenv(env_path)

def get_api_key(service: str) -> Optional[str]:
    """
    Get API key for a service from environment variables.
    
    Args:
        service: Service name (e.g., 'PEXELS', 'PIXABAY')
        
    Returns:
        API key if found, None otherwise
    """
    key = f'{service.upper()}_API_KEY'
    return os.getenv(key)

def save_config(config: Dict[str, Any], config_path: Path) -> None:
    """
    Save configuration to YAML file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save config file
    """
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
