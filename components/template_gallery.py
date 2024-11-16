import streamlit as st
from typing import Dict, Any, List, Type
from ..templates.base_template import VideoTemplate
from ..templates.modern_template import ModernTemplate
from ..templates.minimal_template import MinimalTemplate
from ..templates.dynamic_template import DynamicTemplate

class TemplateGallery:
    """Gallery component for video templates."""
    
    TEMPLATES: Dict[str, Type[VideoTemplate]] = {
        'Modern': ModernTemplate,
        'Minimal': MinimalTemplate,
        'Dynamic': DynamicTemplate
    }
    
    TEMPLATE_DESCRIPTIONS: Dict[str, str] = {
        'Modern': """
        A professional template with smooth transitions and modern design elements.
        Perfect for business and educational content.
        Features:
        - Clean text animations
        - Professional transitions
        - Subtle overlays
        """,
        'Minimal': """
        A clean, minimalist template that puts your content first.
        Ideal for storytelling and artistic content.
        Features:
        - Simple animations
        - Elegant typography
        - Distraction-free design
        """,
        'Dynamic': """
        An energetic template with eye-catching effects.
        Great for social media and entertainment content.
        Features:
        - Dynamic transitions
        - Animated text effects
        - Motion elements
        """
    }
    
    PREVIEW_IMAGES: Dict[str, str] = {
        'Modern': 'assets/previews/modern.jpg',
        'Minimal': 'assets/previews/minimal.jpg',
        'Dynamic': 'assets/previews/dynamic.jpg'
    }
    
    @classmethod
    def render(cls) -> Type[VideoTemplate]:
        """Render the template gallery and return the selected template class."""
        st.header("Choose a Template")
        
        # Create columns for template selection
        cols = st.columns(len(cls.TEMPLATES))
        
        selected_template = None
        
        # Display template options
        for i, (name, template_class) in enumerate(cls.TEMPLATES.items()):
            with cols[i]:
                st.subheader(name)
                
                # Display preview image if available
                if name in cls.PREVIEW_IMAGES:
                    try:
                        st.image(cls.PREVIEW_IMAGES[name], use_column_width=True)
                    except:
                        st.info("Preview image not available")
                
                # Display template description
                st.markdown(cls.TEMPLATE_DESCRIPTIONS[name])
                
                # Display template configuration
                with st.expander("Template Settings"):
                    config = template_class.get_default_config()
                    st.json(config)
                
                # Select button
                if st.button(f"Use {name} Template", key=f"template_{name}"):
                    selected_template = template_class
                    st.success(f"Selected {name} template!")
        
        return selected_template
    
    @staticmethod
    def preview_template(template: Type[VideoTemplate], video_path: str) -> None:
        """Preview the selected template with a sample video."""
        if video_path and st.button("Generate Preview"):
            with st.spinner("Generating preview..."):
                # TODO: Implement preview generation
                st.info("Preview generation coming soon!")
                
    @staticmethod
    def get_template_config(template: Type[VideoTemplate]) -> Dict[str, Any]:
        """Get and customize template configuration."""
        if not template:
            return {}
            
        st.subheader("Template Configuration")
        config = template.get_default_config()
        
        # Allow customization of basic parameters
        with st.expander("Customize Template"):
            if 'dimensions' in config:
                width, height = config['dimensions']
                new_width = st.number_input("Width", value=width, min_value=360, max_value=3840)
                new_height = st.number_input("Height", value=height, min_value=360, max_value=3840)
                config['dimensions'] = (new_width, new_height)
            
            if 'duration' in config:
                config['duration'] = st.number_input(
                    "Duration (seconds)",
                    value=config['duration'],
                    min_value=5,
                    max_value=300
                )
            
            if 'transitions' in config:
                config['transitions']['duration'] = st.slider(
                    "Transition Duration",
                    min_value=0.1,
                    max_value=2.0,
                    value=float(config['transitions'].get('duration', 0.5)),
                    step=0.1
                )
        
        return config
