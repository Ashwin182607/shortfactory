"""
Model Manager for handling AI model fallbacks and caching.
"""
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import torch
from diskcache import Cache
from tenacity import retry, stop_after_attempt, wait_exponential
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    BloomForCausalLM,
    GPTNeoForCausalLM,
    OPTForCausalLM,
    Pipeline,
    T5ForConditionalGeneration,
    pipeline,
)

logger = logging.getLogger(__name__)

# Initialize cache
CACHE_DIR = Path.home() / ".cache" / "shortfactory"
cache = Cache(str(CACHE_DIR / "model_cache"))

class ModelType(Enum):
    SCRIPT_GEN = "script_generation"
    TEXT_CLASS = "text_classification"
    STYLE_TRANSFER = "style_transfer"

class ModelManager:
    """Manages AI models with fallback chain and caching."""
    
    def __init__(self):
        self.models: Dict[ModelType, List[Dict[str, Any]]] = {
            ModelType.SCRIPT_GEN: [
                {
                    "name": "gpt-neo-125m",
                    "model_id": "EleutherAI/gpt-neo-125M",
                    "model_class": GPTNeoForCausalLM,
                    "type": "causal",
                },
                {
                    "name": "bloom-560m",
                    "model_id": "bigscience/bloom-560m",
                    "model_class": BloomForCausalLM,
                    "type": "causal",
                },
                {
                    "name": "opt-350m",
                    "model_id": "facebook/opt-350m",
                    "model_class": OPTForCausalLM,
                    "type": "causal",
                },
                {
                    "name": "t5-small",
                    "model_id": "t5-small",
                    "model_class": T5ForConditionalGeneration,
                    "type": "seq2seq",
                },
                {
                    "name": "flan-t5-small",
                    "model_id": "google/flan-t5-small",
                    "model_class": T5ForConditionalGeneration,
                    "type": "seq2seq",
                },
            ],
            ModelType.TEXT_CLASS: [
                {
                    "name": "distilbert-base",
                    "model_id": "distilbert-base-uncased",
                    "task": "text-classification",
                },
                {
                    "name": "tinybert",
                    "model_id": "huawei-noah/TinyBERT_General_4L_312D",
                    "task": "text-classification",
                },
                {
                    "name": "minilm",
                    "model_id": "microsoft/MiniLM-L12-H384-uncased",
                    "task": "text-classification",
                },
            ],
        }
        self.loaded_models: Dict[str, Pipeline] = {}
        self._initialize_cache()

    def _initialize_cache(self):
        """Initialize the model cache directory."""
        os.makedirs(CACHE_DIR, exist_ok=True)
        logger.info(f"Initialized model cache at {CACHE_DIR}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def get_model(
        self, model_type: ModelType, force_reload: bool = False
    ) -> Optional[Pipeline]:
        """
        Get a model from the fallback chain.
        Attempts each model in the chain until one succeeds.
        """
        models = self.models.get(model_type, [])
        
        for model_config in models:
            try:
                model_name = model_config["name"]
                
                # Check cache first
                if not force_reload and model_name in self.loaded_models:
                    logger.info(f"Using cached model: {model_name}")
                    return self.loaded_models[model_name]
                
                # Load model based on type
                if model_type == ModelType.SCRIPT_GEN:
                    pipeline_task = "text-generation"
                    model = self._load_generation_model(model_config)
                elif model_type == ModelType.TEXT_CLASS:
                    pipeline_task = model_config["task"]
                    model = None  # Let pipeline handle model loading
                
                # Create pipeline
                model_pipeline = pipeline(
                    task=pipeline_task,
                    model=model if model else model_config["model_id"],
                    tokenizer=model_config["model_id"],
                    device=0 if torch.cuda.is_available() else -1,
                )
                
                # Cache the model
                self.loaded_models[model_name] = model_pipeline
                logger.info(f"Successfully loaded model: {model_name}")
                return model_pipeline
                
            except Exception as e:
                logger.warning(f"Failed to load model {model_config['name']}: {str(e)}")
                continue
        
        logger.error(f"All models failed for type {model_type}")
        return None

    def _load_generation_model(self, model_config: Dict[str, Any]):
        """Load a text generation model."""
        if model_config["type"] == "causal":
            model = model_config["model_class"].from_pretrained(
                model_config["model_id"],
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=True,
            )
        else:  # seq2seq
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_config["model_id"],
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=True,
            )
        return model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def generate_text(
        self,
        prompt: str,
        max_length: int = 100,
        model_type: ModelType = ModelType.SCRIPT_GEN,
    ) -> Optional[str]:
        """Generate text using the fallback chain of models."""
        model = await self.get_model(model_type)
        if not model:
            return None
            
        try:
            # Check cache
            cache_key = f"text_gen_{hash(prompt)}_{max_length}"
            if cache_key in cache:
                return cache[cache_key]
            
            # Generate text
            result = model(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
            )
            
            generated_text = result[0]["generated_text"]
            
            # Cache result
            cache[cache_key] = generated_text
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}")
            return None

    async def classify_text(
        self, text: str, labels: List[str]
    ) -> Optional[Dict[str, float]]:
        """Classify text using the fallback chain of models."""
        model = await self.get_model(ModelType.TEXT_CLASS)
        if not model:
            return None
            
        try:
            # Check cache
            cache_key = f"text_class_{hash(text)}_{hash(str(labels))}"
            if cache_key in cache:
                return cache[cache_key]
            
            # Classify text
            result = model(text, labels)
            
            # Format result
            classifications = {
                label: score
                for label, score in zip(result["labels"], result["scores"])
            }
            
            # Cache result
            cache[cache_key] = classifications
            
            return classifications
            
        except Exception as e:
            logger.error(f"Text classification failed: {str(e)}")
            return None

    def clear_cache(self):
        """Clear the model cache."""
        cache.clear()
        logger.info("Model cache cleared")
