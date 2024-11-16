#!/usr/bin/env python3
import os
import logging
from gui.main_ui import ShortFactoryUI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    load_dotenv()
    
    # Create necessary directories
    os.makedirs('assets/previews', exist_ok=True)
    os.makedirs('assets/music', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
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

if __name__ == "__main__":
    main()
