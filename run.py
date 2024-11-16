import os
from gui.main_ui import ShortFactoryUI
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Create necessary directories
    os.makedirs('assets/previews', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # Initialize and launch UI
    ui = ShortFactoryUI()
    ui.queue()  # Enable queueing for concurrent operations
    ui.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,  # Default Gradio port
        share=True,  # Create public link
        inbrowser=True  # Open in browser automatically
    )

if __name__ == "__main__":
    main()
