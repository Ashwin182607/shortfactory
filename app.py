import streamlit as st
from components.template_gallery import TemplateGallery
from engines.video_engine import VideoEngine
from utils.script_generator import ScriptGenerator
from utils.asset_sourcing import AssetManager
from utils.music_manager import MusicManager
import os

st.set_page_config(page_title="ShortFactory", page_icon="🎬", layout="wide")

def main():
    st.title("🎬 ShortFactory")
    st.markdown("Create engaging social media videos with AI")
    
    # Initialize session state
    if 'video_engine' not in st.session_state:
        st.session_state.video_engine = VideoEngine()
    if 'template' not in st.session_state:
        st.session_state.template = None
    
    # Sidebar for project settings
    with st.sidebar:
        st.header("Project Settings")
        platform = st.selectbox(
            "Target Platform",
            ["YouTube Shorts", "Instagram Reels", "TikTok"]
        )
        
        topic = st.text_input("Video Topic", placeholder="Enter your video topic...")
        
        if st.button("Generate Script"):
            with st.spinner("Generating script..."):
                script = ScriptGenerator.generate(topic, platform)
                st.session_state.script = script
                st.success("Script generated!")
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["Template", "Content", "Export"])
    
    # Template Selection Tab
    with tab1:
        template = TemplateGallery.render()
        if template:
            st.session_state.template = template
            
        if st.session_state.template:
            config = TemplateGallery.get_template_config(st.session_state.template)
            st.session_state.config = config
    
    # Content Creation Tab
    with tab2:
        if not st.session_state.template:
            st.warning("Please select a template first!")
            return
            
        st.header("Content Creation")
        
        # Script Section
        st.subheader("Script")
        if 'script' in st.session_state:
            script = st.text_area("Edit Script", st.session_state.script, height=200)
        else:
            script = st.text_area("Enter Script", height=200)
        
        # Asset Selection
        st.subheader("Video Assets")
        uploaded_video = st.file_uploader("Upload Video", type=['mp4', 'mov'])
        
        if not uploaded_video:
            st.info("No video uploaded. We'll source relevant clips based on your script.")
            if st.button("Source Video Clips"):
                with st.spinner("Searching for relevant clips..."):
                    clips = AssetManager.source_video_clips(script)
                    st.session_state.clips = clips
                    st.success("Found relevant clips!")
        
        # Music Selection
        st.subheader("Background Music")
        music_style = st.selectbox(
            "Music Style",
            ["Energetic", "Calm", "Inspirational", "Dramatic"]
        )
        
        if st.button("Find Music"):
            with st.spinner("Searching for music..."):
                music = MusicManager.find_music(style=music_style)
                st.session_state.music = music
                st.success("Found matching music!")
    
    # Export Tab
    with tab3:
        if not st.session_state.template:
            st.warning("Please select a template first!")
            return
            
        st.header("Export Video")
        
        # Preview section
        st.subheader("Preview")
        if 'clips' in st.session_state:
            TemplateGallery.preview_template(
                st.session_state.template,
                st.session_state.clips[0] if st.session_state.clips else None
            )
        
        # Export settings
        st.subheader("Export Settings")
        quality = st.select_slider(
            "Quality",
            options=["Draft", "Standard", "High Quality"],
            value="Standard"
        )
        
        export_platform = st.multiselect(
            "Export For",
            ["YouTube Shorts", "Instagram Reels", "TikTok"],
            default=[platform]
        )
        
        if st.button("Export Video"):
            with st.spinner("Creating your video..."):
                try:
                    # Create video with selected template and settings
                    video_engine = st.session_state.video_engine
                    video_path = video_engine.create_video(
                        template=st.session_state.template,
                        config=st.session_state.config,
                        script=script,
                        clips=st.session_state.clips if 'clips' in st.session_state else None,
                        music=st.session_state.music if 'music' in st.session_state else None,
                        quality=quality,
                        platforms=export_platform
                    )
                    
                    # Offer download
                    with open(video_path, 'rb') as f:
                        st.download_button(
                            "Download Video",
                            f,
                            file_name="shortfactory_video.mp4",
                            mime="video/mp4"
                        )
                        
                    st.success("Video created successfully!")
                    
                except Exception as e:
                    st.error(f"Error creating video: {str(e)}")

if __name__ == "__main__":
    main()
