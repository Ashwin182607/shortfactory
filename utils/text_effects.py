from typing import Tuple, List, Dict, Any
from moviepy.editor import TextClip, CompositeVideoClip, VideoClip, ColorClip
import numpy as np

class TextEffects:
    @staticmethod
    def create_caption(
        text: str,
        size: Tuple[int, int],
        fontsize: int = 30,
        color: str = 'white',
        font: str = 'Arial',
        stroke_color: str = 'black',
        stroke_width: int = 2,
    ) -> TextClip:
        """
        Create a caption with outline effect.
        
        Args:
            text (str): Caption text
            size (Tuple[int, int]): Video dimensions (width, height)
            fontsize (int): Font size
            color (str): Text color
            font (str): Font name
            stroke_color (str): Outline color
            stroke_width (int): Outline width
            
        Returns:
            TextClip: MoviePy text clip
        """
        return TextClip(
            text,
            fontsize=fontsize,
            color=color,
            font=font,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            size=size,
            method='caption',
            align='center'
        )
    
    @staticmethod
    def create_title(
        text: str,
        size: Tuple[int, int],
        fontsize: int = 50,
        color: str = 'white',
        font: str = 'Arial-Bold',
        bg_color: str = 'black',
        bg_opacity: float = 0.5
    ) -> CompositeVideoClip:
        """
        Create a title with background.
        
        Args:
            text (str): Title text
            size (Tuple[int, int]): Video dimensions
            fontsize (int): Font size
            color (str): Text color
            font (str): Font name
            bg_color (str): Background color
            bg_opacity (float): Background opacity
            
        Returns:
            CompositeVideoClip: Composite clip with text and background
        """
        # Create text clip
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            color=color,
            font=font,
            size=size,
            method='caption',
            align='center'
        )
        
        # Create background
        bg = ColorClip(size, bg_color).set_opacity(bg_opacity)
        
        return CompositeVideoClip([bg, txt_clip])
    
    @staticmethod
    def animate_text(
        clip: TextClip,
        effect: str = 'fade',
        duration: float = 3.0,
        **kwargs
    ) -> TextClip:
        """
        Apply animation effect to text.
        
        Args:
            clip (TextClip): Text clip to animate
            effect (str): Animation effect name
            duration (float): Effect duration
            **kwargs: Additional effect parameters
            
        Returns:
            TextClip: Animated text clip
        """
        effects = {
            'fade': lambda c: c.fadeout(kwargs.get('fade_duration', 0.5))
                            .fadein(kwargs.get('fade_duration', 0.5)),
            'slide': lambda c: c.set_position(
                lambda t: ('center', 50 + t * 100) if t < duration/2
                else ('center', 150 - (t-duration/2) * 100)
            ),
            'zoom': lambda c: c.resize(
                lambda t: 1 + 0.3 * np.sin(t * 2 * np.pi / duration)
            ),
            'typewriter': lambda c: c.set_mask(
                lambda t: np.array([[[1 if j/c.w < t/duration else 0
                    for j in range(c.w)]
                    for i in range(c.h)]])
            ),
            'bounce': lambda c: c.set_position(
                lambda t: ('center', 100 + 50 * abs(np.sin(t * 2 * np.pi / duration)))
            ),
            'rotate': lambda c: c.rotate(
                lambda t: 360 * t / duration
            ),
            'wave': lambda c: c.set_position(
                lambda t: ('center', 100 + 30 * np.sin(t * 4 * np.pi / duration + c.w))
            ),
            'glitch': lambda c: c.set_position(
                lambda t: ('center', 100 + (5 * np.random.randn() if t % 0.2 < 0.1 else 0))
            ),
            'split': lambda c: c.set_position(
                lambda t: (('center', 100) if t > duration/2
                         else ('center' if t > duration/4 else 'left', 100))
            )
        }
        
        return effects.get(effect, effects['fade'])(clip)
    
    @staticmethod
    def add_captions_to_video(
        video: VideoClip,
        captions: List[Dict[str, Any]]
    ) -> CompositeVideoClip:
        """
        Add multiple captions to video.
        
        Args:
            video (VideoClip): Input video
            captions (List[Dict[str, Any]]): List of caption configurations
                Each dict should have:
                - text: Caption text
                - start: Start time
                - end: End time
                - position: Position ('top', 'bottom', or tuple)
                - style: Optional style parameters
                
        Returns:
            CompositeVideoClip: Video with captions
        """
        clips = [video]
        
        for cap in captions:
            text = cap['text']
            start = cap['start']
            end = cap['end']
            position = cap.get('position', 'bottom')
            style = cap.get('style', {})
            
            # Create caption clip
            txt_clip = TextEffects.create_caption(
                text,
                video.size,
                **style
            )
            
            # Set timing
            txt_clip = txt_clip.set_start(start).set_end(end)
            
            # Set position
            if position == 'top':
                txt_clip = txt_clip.set_position(('center', 50))
            elif position == 'bottom':
                txt_clip = txt_clip.set_position(('center', video.h - 100))
            else:
                txt_clip = txt_clip.set_position(position)
            
            clips.append(txt_clip)
        
        return CompositeVideoClip(clips)

    @staticmethod
    def create_overlay(
        size: Tuple[int, int],
        style: str = 'gradient',
        color: str = 'black',
        opacity: float = 0.3
    ) -> VideoClip:
        """
        Create video overlay effect.
        
        Args:
            size (Tuple[int, int]): Video dimensions
            style (str): Overlay style ('solid', 'gradient', 'vignette')
            color (str): Overlay color
            opacity (float): Opacity level
            
        Returns:
            VideoClip: Overlay clip
        """
        width, height = size
        
        if style == 'gradient':
            gradient = np.linspace(0, 1, height)[:, np.newaxis] * np.ones((height, width))
            mask = ColorClip(size, color).set_opacity(opacity)
            mask = mask.set_mask(lambda t: gradient)
            return mask
        
        elif style == 'vignette':
            x = np.linspace(-1, 1, width)
            y = np.linspace(-1, 1, height)
            X, Y = np.meshgrid(x, y)
            R = np.sqrt(X**2 + Y**2)
            vignette = np.clip(1 - R, 0, 1)
            mask = ColorClip(size, color).set_opacity(opacity)
            mask = mask.set_mask(lambda t: vignette)
            return mask
        
        else:  # solid
            return ColorClip(size, color).set_opacity(opacity)
