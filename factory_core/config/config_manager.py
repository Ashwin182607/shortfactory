"""
Configuration Manager for ShortFactory.
"""
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages configuration settings and environment variables."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self.root_dir = Path(__file__).parent.parent.parent
        self.config_file = self.root_dir / "config.json"
        self.env_file = self.root_dir / ".env"
        
        # Default configuration
        self.defaults = {
            "output_dir": str(self.root_dir / "output"),
            "cache_dir": str(self.root_dir / ".cache"),
            "models_dir": str(self.root_dir / "models"),
            "assets_dir": str(self.root_dir / "assets"),
            "web_interface": {
                "host": "0.0.0.0",
                "port": 7860,
                "share": True,
                "auth": None,
            },
            "video": {
                "resolution": [1080, 1920],
                "fps": 30,
                "max_duration": 60,
            },
            "audio": {
                "sample_rate": 44100,
                "channels": 2,
            },
            "api": {
                "pexels": "",
                "pixabay": "",
                "unsplash": "",
            }
        }
        
        # Load configuration
        self.config = self.defaults.copy()
        self._load_config()
        self._load_env()
        
        # Create directories
        self._create_directories()
    
    def _load_config(self):
        """Load configuration from JSON file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                self.config.update(user_config)
                logger.info("Configuration loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load configuration: {e}")
    
    def _load_env(self):
        """Load environment variables."""
        load_dotenv(self.env_file)
        
        # Update API keys from environment
        self.config["api"]["pexels"] = os.getenv("PEXELS_API_KEY", "")
        self.config["api"]["pixabay"] = os.getenv("PIXABAY_API_KEY", "")
        self.config["api"]["unsplash"] = os.getenv("UNSPLASH_API_KEY", "")
    
    def _create_directories(self):
        """Create necessary directories."""
        directories = [
            self.config["output_dir"],
            self.config["cache_dir"],
            self.config["models_dir"],
            self.config["assets_dir"],
            os.path.join(self.config["assets_dir"], "videos"),
            os.path.join(self.config["assets_dir"], "music"),
            os.path.join(self.config["assets_dir"], "images"),
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        try:
            value = self.config
            for k in key.split('.'):
                value = value[k]
            return value
        except KeyError:
            return default
    
    def set(self, key: str, value: Any):
        """Set a configuration value."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        
        # Save to file
        self.save()
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def update_api_key(self, service: str, key: str):
        """Update API key for a service."""
        if service not in self.config["api"]:
            raise ValueError(f"Unknown service: {service}")
        
        # Update configuration
        self.config["api"][service] = key
        
        # Update environment file
        env_key = f"{service.upper()}_API_KEY"
        env_lines = []
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                env_lines = f.readlines()
        
        # Find and replace or append key
        key_found = False
        for i, line in enumerate(env_lines):
            if line.startswith(f"{env_key}="):
                env_lines[i] = f"{env_key}={key}\n"
                key_found = True
                break
        
        if not key_found:
            env_lines.append(f"{env_key}={key}\n")
        
        # Write back to file
        with open(self.env_file, 'w') as f:
            f.writelines(env_lines)
        
        # Reload environment
        load_dotenv(override=True)
        logger.info(f"API key updated for {service}")
    
    def reset(self):
        """Reset configuration to defaults."""
        self.config = self.defaults.copy()
        self.save()
        logger.info("Configuration reset to defaults")
