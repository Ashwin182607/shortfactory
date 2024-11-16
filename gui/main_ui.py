import gradio as gr
from .ui_abstract_base import UIPage
from .ui_components_html import get_html_header
from factory_core.engine.video_engine import VideoEngine
from factory_core.ai.script_generator import ScriptGenerator
from utils.asset_sourcing import AssetManager
from utils.music_manager import MusicManager
from templates.modern_template import ModernTemplate
from templates.minimal_template import MinimalTemplate
from templates.dynamic_template import DynamicTemplate
from templates.ai_dynamic_template import AIDynamicTemplate

class ShortFactoryUI(UIPage):
    """Main UI for ShortFactory"""
    
    TEMPLATES = {
        'Modern': ModernTemplate,
        'Minimal': MinimalTemplate,
        'Dynamic': DynamicTemplate,
        'AI Dynamic': AIDynamicTemplate
    }
    
    def __init__(self):
        self.video_engine = VideoEngine()
        super().__init__()
    
    def init_components(self):
        """Initialize UI components"""
        # Template configs
        self.template_configs = {
            name: {
                'dimensions': (1080, 1920),
                'duration': 30,
                'style': 'modern',
                'transition_duration': 0.5,
                'text_duration': 3.0
            } for name in self.TEMPLATES.keys()
        }
    
    def create_ui(self):
        """Create the main UI"""
        with gr.Blocks(css=".container { max-width: 1100px; margin: auto; }") as interface:
            # Header
            gr.HTML(get_html_header())
            
            # Main tabs
            with gr.Tabs():
                # Video Creation Tab
                with gr.Tab("Create Video"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            # Input settings
                            platform = gr.Dropdown(
                                choices=["YouTube Shorts", "Instagram Reels", "TikTok"],
                                label="Platform",
                                value="YouTube Shorts"
                            )
                            topic = gr.Textbox(
                                label="Video Topic",
                                placeholder="Enter your video topic or idea..."
                            )
                            generate_btn = gr.Button("Generate Script", variant="primary")
                            
                            # Template selection
                            template = gr.Dropdown(
                                choices=list(self.TEMPLATES.keys()),
                                label="Video Template",
                                value="Modern"
                            )
                            
                            # Advanced settings
                            with gr.Accordion("Advanced Settings", open=False):
                                duration = gr.Slider(
                                    minimum=15,
                                    maximum=60,
                                    value=30,
                                    step=15,
                                    label="Video Duration (seconds)"
                                )
                                quality = gr.Radio(
                                    choices=["Draft", "Standard", "High Quality"],
                                    value="Standard",
                                    label="Video Quality"
                                )
                                
                        with gr.Column(scale=2):
                            # Script editor
                            script = gr.TextArea(
                                label="Script",
                                placeholder="Your video script will appear here...",
                                lines=10
                            )
                            
                            # Asset preview
                            preview = gr.Image(label="Preview", visible=False)
                            
                            # Status and progress
                            status = gr.Markdown("Ready to create your video!")
                            progress = gr.Progress(visible=False)
                    
                    with gr.Row():
                        # Asset controls
                        gr.Markdown("### Video Assets")
                        upload_video = gr.File(
                            label="Upload Video",
                            file_types=["video"],
                            visible=True
                        )
                        source_video_btn = gr.Button("Source Video Clips")
                        
                        # Music controls
                        gr.Markdown("### Background Music")
                        music_style = gr.Dropdown(
                            choices=["Energetic", "Calm", "Inspirational", "Dramatic"],
                            label="Music Style",
                            value="Energetic"
                        )
                        source_music_btn = gr.Button("Find Music")
                    
                    # Create video button
                    create_btn = gr.Button("Create Video", variant="primary", size="large")
                    
                    # Output video
                    output_video = gr.Video(label="Generated Video")
                
                # Asset Library Tab
                with gr.Tab("Asset Library"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### Saved Videos")
                            # Add asset library components here
                
                # Settings Tab
                with gr.Tab("Settings"):
                    with gr.Row():
                        with gr.Column():
                            api_key_pexels = gr.Textbox(
                                label="Pexels API Key",
                                type="password"
                            )
                            api_key_pixabay = gr.Textbox(
                                label="Pixabay API Key",
                                type="password"
                            )
                            save_keys_btn = gr.Button("Save API Keys")
            
            # Event handlers
            def generate_script(topic, platform):
                try:
                    script = ScriptGenerator.generate(topic, platform)
                    return script, "Script generated successfully!"
                except Exception as e:
                    return "", f"Error generating script: {str(e)}"
            
            def source_videos(script):
                try:
                    clips = AssetManager.source_video_clips(script)
                    preview_path = clips[0] if clips else None
                    return (
                        gr.Image.update(value=preview_path, visible=True),
                        "Video clips sourced successfully!"
                    )
                except Exception as e:
                    return None, f"Error sourcing videos: {str(e)}"
            
            def source_music(style):
                try:
                    music = MusicManager.find_music(style=style)
                    return "Music track found successfully!"
                except Exception as e:
                    return f"Error finding music: {str(e)}"
            
            def create_video(
                template_name,
                script,
                duration,
                quality,
                platform,
                progress=gr.Progress()
            ):
                try:
                    template_class = self.TEMPLATES[template_name]
                    config = self.template_configs[template_name].copy()
                    config['duration'] = duration
                    
                    progress(0, desc="Starting video creation...")
                    
                    # Create video
                    video_path = self.video_engine.create_video(
                        template=template_class,
                        config=config,
                        script=script,
                        quality=quality,
                        platforms=[platform]
                    )
                    
                    progress(1, desc="Video created successfully!")
                    return video_path, "Video created successfully!"
                    
                except Exception as e:
                    return None, f"Error creating video: {str(e)}"
            
            # Connect event handlers
            generate_btn.click(
                generate_script,
                inputs=[topic, platform],
                outputs=[script, status]
            )
            
            source_video_btn.click(
                source_videos,
                inputs=[script],
                outputs=[preview, status]
            )
            
            source_music_btn.click(
                source_music,
                inputs=[music_style],
                outputs=[status]
            )
            
            create_btn.click(
                create_video,
                inputs=[
                    template,
                    script,
                    duration,
                    quality,
                    platform
                ],
                outputs=[output_video, status]
            )
        
        return interface
