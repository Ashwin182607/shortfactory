"""
Web interface for ShortFactory using Gradio.
"""
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import gradio as gr
from dotenv import load_dotenv

from factory_core.factory import ShortFactory
from factory_core.ai.style_manager import VideoStyle
from factory_core.effects.text_effects import TextEffect, TextPosition

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShortFactoryUI:
    def __init__(self):
        self.factory = ShortFactory()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Default settings
        self.default_duration = 30
        self.available_styles = [style.value for style in VideoStyle]
        self.available_effects = [effect.value for effect in TextEffect]
        self.available_positions = [pos.value for pos in TextPosition]

    def create_interface(self):
        """Create the Gradio interface."""
        with gr.Blocks(title="ShortFactory - AI Video Creator") as interface:
            gr.Markdown("""
            # 🎬 ShortFactory
            ### AI-Powered Video Content Creation
            Create engaging short-form videos for social media platforms automatically!
            """)
            
            with gr.Tabs():
                # Video Creation Tab
                with gr.Tab("Create Video"):
                    with gr.Row():
                        with gr.Column():
                            topic = gr.Textbox(
                                label="Topic/Prompt",
                                placeholder="Enter your video topic or prompt..."
                            )
                            platform = gr.Dropdown(
                                choices=["YouTube Shorts", "TikTok", "Instagram Reels"],
                                label="Platform"
                            )
                            style = gr.Dropdown(
                                choices=self.available_styles,
                                label="Video Style"
                            )
                            duration = gr.Slider(
                                minimum=15,
                                maximum=60,
                                value=self.default_duration,
                                label="Duration (seconds)"
                            )
                            
                            # Text Effects Section
                            gr.Markdown("### Text Effects")
                            effect_type = gr.Dropdown(
                                choices=self.available_effects,
                                label="Text Effect"
                            )
                            text_position = gr.Dropdown(
                                choices=self.available_positions,
                                label="Text Position"
                            )
                            
                            create_btn = gr.Button(
                                "Create Video",
                                variant="primary"
                            )
                        
                        with gr.Column():
                            output_video = gr.Video(label="Generated Video")
                            status = gr.Textbox(
                                label="Status",
                                interactive=False
                            )
                
                # Settings Tab
                with gr.Tab("Settings"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### API Keys")
                            pexels_key = gr.Textbox(
                                label="Pexels API Key",
                                type="password",
                                value=os.getenv("PEXELS_API_KEY", "")
                            )
                            pixabay_key = gr.Textbox(
                                label="Pixabay API Key",
                                type="password",
                                value=os.getenv("PIXABAY_API_KEY", "")
                            )
                            save_keys_btn = gr.Button("Save API Keys")
                
                # Help Tab
                with gr.Tab("Help"):
                    gr.Markdown("""
                    ### 📚 How to Use ShortFactory
                    
                    1. **Enter Topic/Prompt**
                       - Be specific about what you want in your video
                       - Example: "5 amazing facts about space exploration"
                    
                    2. **Choose Platform**
                       - Select your target platform
                       - Each platform has optimized settings
                    
                    3. **Select Style**
                       - Choose from various video styles
                       - Affects visual appearance and mood
                    
                    4. **Set Duration**
                       - Choose video length (15-60 seconds)
                       - Platform guidelines are automatically applied
                    
                    5. **Text Effects**
                       - Choose animation style for text overlays
                       - Select text positioning
                    
                    ### 🔑 API Keys
                    
                    - Pexels and Pixabay keys are required for video assets
                    - Get free API keys from:
                      - [Pexels](https://www.pexels.com/api/)
                      - [Pixabay](https://pixabay.com/api/docs/)
                    
                    ### 🚀 Tips
                    
                    - Use clear, engaging prompts
                    - Match style to content type
                    - Consider platform-specific trends
                    - Test different text effects
                    """)
            
            # Event handlers
            create_btn.click(
                fn=self.create_video,
                inputs=[
                    topic,
                    platform,
                    style,
                    duration,
                    effect_type,
                    text_position
                ],
                outputs=[output_video, status]
            )
            
            save_keys_btn.click(
                fn=self.save_api_keys,
                inputs=[pexels_key, pixabay_key],
                outputs=[status]
            )
        
        return interface

    def create_video(
        self,
        topic: str,
        platform: str,
        style: str,
        duration: int,
        effect_type: str,
        text_position: str
    ) -> Tuple[str, str]:
        """Create a video using ShortFactory."""
        try:
            # Update status
            yield None, "Generating video script..."
            
            # Generate video
            output_path = self.factory.create_video(
                topic=topic,
                platform=platform,
                style=style,
                duration=duration,
                text_effect=effect_type,
                text_position=text_position
            )
            
            return str(output_path), "Video generated successfully!"
        
        except Exception as e:
            logger.error(f"Error creating video: {str(e)}")
            return None, f"Error: {str(e)}"

    def save_api_keys(
        self,
        pexels_key: str,
        pixabay_key: str
    ) -> str:
        """Save API keys to .env file."""
        try:
            env_path = Path(".env")
            
            # Read existing content
            if env_path.exists():
                with open(env_path, "r") as f:
                    lines = f.readlines()
            else:
                lines = []
            
            # Update or add keys
            keys = {
                "PEXELS_API_KEY": pexels_key,
                "PIXABAY_API_KEY": pixabay_key
            }
            
            new_lines = []
            for line in lines:
                key = line.split("=")[0].strip()
                if key not in keys:
                    new_lines.append(line)
            
            # Add new keys
            for key, value in keys.items():
                if value:  # Only add non-empty keys
                    new_lines.append(f"{key}={value}\n")
            
            # Write back to file
            with open(env_path, "w") as f:
                f.writelines(new_lines)
            
            return "API keys saved successfully!"
        
        except Exception as e:
            logger.error(f"Error saving API keys: {str(e)}")
            return f"Error saving API keys: {str(e)}"

def main():
    """Launch the web interface."""
    ui = ShortFactoryUI()
    interface = ui.create_interface()
    interface.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860,
        auth=None  # Add authentication if needed
    )

if __name__ == "__main__":
    main()
