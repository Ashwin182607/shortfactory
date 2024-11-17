#!/usr/bin/env python3
"""
Launch script for ShortFactory
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check for required dependencies."""
    try:
        import torch
        import transformers
        import gradio
        import moviepy
        logger.info(" Core dependencies found")
        return True
    except ImportError as e:
        logger.error(f" Missing dependency: {str(e)}")
        logger.info("Installing dependencies...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        return False

def check_api_keys():
    """Check for required API keys."""
    load_dotenv()
    required_keys = ["PEXELS_API_KEY", "PIXABAY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        logger.warning(f" Missing API keys: {', '.join(missing_keys)}")
        logger.info("You can still use ShortFactory, but some features will be limited.")
        return False
    return True

def check_directories():
    """Check and create required directories."""
    required_dirs = [
        "assets/videos",
        "assets/music",
        "assets/images",
        "models",
        "output"
    ]
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    logger.info(" Directory structure verified")

def main():
    """Main entry point."""
    logger.info(" Starting ShortFactory...")
    
    # Check environment
    check_directories()
    if not check_dependencies():
        logger.error("Failed to install dependencies. Please install manually.")
        sys.exit(1)
    check_api_keys()
    
    # Import after dependency check
    try:
        from gui.main_ui import ShortFactoryUI
        logger.info(" Web interface loaded")
    except ImportError as e:
        logger.error(f"Failed to load web interface: {str(e)}")
        sys.exit(1)
    
    # Launch web interface
    try:
        # Load environment variables
        load_dotenv()
        
        # Create necessary directories
        os.makedirs('assets/previews', exist_ok=True)
        
        # Check for API keys
        pexels_key = os.getenv('PEXELS_API_KEY')
        pixabay_key = os.getenv('PIXABAY_API_KEY')
        
        if not pexels_key or not pixabay_key:
            logger.warning(
                "API keys not found in .env file. "
                "You'll need to add them in the Settings tab."
            )
        
        # Initialize and launch UI
        logger.info("Starting ShortFactory...")
        ui = ShortFactoryUI()
        
        # Launch with Gradio
        ui.launch(
            server_name="0.0.0.0",  # Allow external access
            server_port=7860,  # Default Gradio port
            share=True,  # Create public link
            auth=None,  # No authentication required
            inbrowser=True  # Open in browser automatically
        )
    except Exception as e:
        logger.error(f"Failed to start web interface: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
