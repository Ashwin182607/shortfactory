"""
Style Manager for handling video style transfer with fallbacks.
"""
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union

import torch
import torch.nn as nn
from diskcache import Cache
from fastai.vision.all import load_learner
from tenacity import retry, stop_after_attempt, wait_exponential
from torchvision import transforms
from transformers import AutoImageProcessor, AutoModelForImageProcessing

logger = logging.getLogger(__name__)

# Initialize cache
CACHE_DIR = Path.home() / ".cache" / "shortfactory"
cache = Cache(str(CACHE_DIR / "style_cache"))

class StyleType(Enum):
    CINEMATIC = "cinematic"
    VLOG = "vlog"
    MINIMAL = "minimal"
    DYNAMIC = "dynamic"
    CUSTOM = "custom"

class StyleManager:
    """Manages video style transfer with fallback chain and caching."""
    
    def __init__(self):
        self.models: Dict[StyleType, List[Dict[str, any]]] = {
            StyleType.CINEMATIC: [
                {
                    "name": "fastai-cinematic",
                    "path": "models/cinematic.pkl",
                    "type": "fastai",
                },
                {
                    "name": "stable-diffusion-cinematic",
                    "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
                    "type": "diffusion",
                },
            ],
            StyleType.VLOG: [
                {
                    "name": "fastai-vlog",
                    "path": "models/vlog.pkl",
                    "type": "fastai",
                },
                {
                    "name": "basic-vlog",
                    "type": "basic",
                    "params": {
                        "brightness": 1.2,
                        "contrast": 1.1,
                        "saturation": 1.1,
                    },
                },
            ],
            StyleType.MINIMAL: [
                {
                    "name": "fastai-minimal",
                    "path": "models/minimal.pkl",
                    "type": "fastai",
                },
                {
                    "name": "basic-minimal",
                    "type": "basic",
                    "params": {
                        "brightness": 1.0,
                        "contrast": 1.05,
                        "saturation": 0.9,
                    },
                },
            ],
            StyleType.DYNAMIC: [
                {
                    "name": "fastai-dynamic",
                    "path": "models/dynamic.pkl",
                    "type": "fastai",
                },
                {
                    "name": "basic-dynamic",
                    "type": "basic",
                    "params": {
                        "brightness": 1.1,
                        "contrast": 1.2,
                        "saturation": 1.2,
                    },
                },
            ],
        }
        self.loaded_models: Dict[str, any] = {}
        self._initialize_cache()
        self._initialize_transforms()

    def _initialize_cache(self):
        """Initialize the style cache directory."""
        os.makedirs(CACHE_DIR, exist_ok=True)
        logger.info(f"Initialized style cache at {CACHE_DIR}")

    def _initialize_transforms(self):
        """Initialize image transforms."""
        self.transforms = transforms.Compose([
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225]),
        ])

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def get_style_model(
        self, style_type: StyleType, force_reload: bool = False
    ) -> Optional[Union[nn.Module, Dict]]:
        """Get a style model from the fallback chain."""
        models = self.models.get(style_type, [])
        
        for model_config in models:
            try:
                model_name = model_config["name"]
                
                # Check cache first
                if not force_reload and model_name in self.loaded_models:
                    logger.info(f"Using cached model: {model_name}")
                    return self.loaded_models[model_name]
                
                # Load model based on type
                if model_config["type"] == "fastai":
                    model = await self._load_fastai_model(model_config)
                elif model_config["type"] == "diffusion":
                    model = await self._load_diffusion_model(model_config)
                elif model_config["type"] == "basic":
                    model = model_config["params"]
                else:
                    continue
                
                # Cache the model
                self.loaded_models[model_name] = model
                logger.info(f"Successfully loaded model: {model_name}")
                return model
                
            except Exception as e:
                logger.warning(f"Failed to load model {model_config['name']}: {str(e)}")
                continue
        
        logger.error(f"All style models failed for type {style_type}")
        return None

    async def _load_fastai_model(self, model_config: Dict) -> Optional[nn.Module]:
        """Load a FastAI style model."""
        try:
            model = load_learner(model_config["path"])
            return model
        except Exception as e:
            logger.error(f"Failed to load FastAI model: {str(e)}")
            return None

    async def _load_diffusion_model(self, model_config: Dict) -> Optional[nn.Module]:
        """Load a diffusion model."""
        try:
            processor = AutoImageProcessor.from_pretrained(model_config["model_id"])
            model = AutoModelForImageProcessing.from_pretrained(
                model_config["model_id"],
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            )
            return {"model": model, "processor": processor}
        except Exception as e:
            logger.error(f"Failed to load diffusion model: {str(e)}")
            return None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def apply_style(
        self,
        frames: torch.Tensor,
        style_type: StyleType,
        strength: float = 1.0,
    ) -> Optional[torch.Tensor]:
        """Apply style transfer to video frames."""
        model = await self.get_style_model(style_type)
        if not model:
            return None
            
        try:
            # Check cache
            cache_key = f"style_{style_type.value}_{hash(str(frames.shape))}_{strength}"
            if cache_key in cache:
                return cache[cache_key]
            
            # Apply style based on model type
            if isinstance(model, dict) and "brightness" in model:
                # Basic style
                styled_frames = self._apply_basic_style(frames, model, strength)
            elif isinstance(model, dict) and "model" in model:
                # Diffusion model
                styled_frames = await self._apply_diffusion_style(
                    frames, model, strength
                )
            else:
                # FastAI model
                styled_frames = await self._apply_fastai_style(frames, model, strength)
            
            # Cache result
            cache[cache_key] = styled_frames
            return styled_frames
            
        except Exception as e:
            logger.error(f"Style transfer failed: {str(e)}")
            return None

    def _apply_basic_style(
        self, frames: torch.Tensor, params: Dict[str, float], strength: float
    ) -> torch.Tensor:
        """Apply basic style adjustments."""
        styled = frames.clone()
        
        # Apply adjustments with strength factor
        for param, value in params.items():
            if param == "brightness":
                styled = styled * (1 + (value - 1) * strength)
            elif param == "contrast":
                mean = styled.mean()
                styled = (styled - mean) * (1 + (value - 1) * strength) + mean
            elif param == "saturation":
                grayscale = styled.mean(dim=1, keepdim=True)
                styled = styled * (1 + (value - 1) * strength) + grayscale * (
                    1 - (1 + (value - 1) * strength)
                )
                
        return torch.clamp(styled, 0, 1)

    async def _apply_fastai_style(
        self, frames: torch.Tensor, model: nn.Module, strength: float
    ) -> torch.Tensor:
        """Apply FastAI style transfer."""
        styled_frames = []
        
        for frame in frames:
            # Apply model
            styled = model.model(frame.unsqueeze(0))
            # Blend with original based on strength
            styled = frame * (1 - strength) + styled * strength
            styled_frames.append(styled)
            
        return torch.stack(styled_frames)

    async def _apply_diffusion_style(
        self, frames: torch.Tensor, model_dict: Dict, strength: float
    ) -> torch.Tensor:
        """Apply diffusion model style transfer."""
        model = model_dict["model"]
        processor = model_dict["processor"]
        styled_frames = []
        
        for frame in frames:
            # Process frame
            inputs = processor(frame, return_tensors="pt")
            # Generate styled frame
            with torch.no_grad():
                styled = model.generate(**inputs)[0]
            # Blend with original based on strength
            styled = frame * (1 - strength) + styled * strength
            styled_frames.append(styled)
            
        return torch.stack(styled_frames)

    def clear_cache(self):
        """Clear the style cache."""
        cache.clear()
        logger.info("Style cache cleared")
