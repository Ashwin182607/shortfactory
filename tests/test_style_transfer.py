"""
Tests for style transfer functionality.
"""
import pytest
import torch
import numpy as np
from pathlib import Path

from factory_core.ai.style_transfer import StyleTransferModel, FastStyleTransfer

@pytest.fixture
def style_model():
    """Create style transfer model instance."""
    return StyleTransferModel()

@pytest.fixture
def fast_style_model():
    """Create fast style transfer model instance."""
    return FastStyleTransfer()

def test_style_model_initialization(style_model):
    """Test style model initialization."""
    assert style_model is not None
    assert len(style_model.blocks) == 5
    assert style_model.device in ['cuda', 'cpu']

def test_fast_style_initialization(fast_style_model):
    """Test fast style model initialization."""
    assert fast_style_model is not None
    assert hasattr(fast_style_model, 'conv1')
    assert hasattr(fast_style_model, 'res1')
    assert hasattr(fast_style_model, 'deconv1')

def test_style_model_forward(style_model):
    """Test style model forward pass."""
    batch_size = 1
    channels = 3
    height = 256
    width = 256
    
    x = torch.randn(batch_size, channels, height, width)
    x = x.to(style_model.device)
    
    features = style_model(x)
    assert len(features) == 5
    for feat in features:
        assert isinstance(feat, torch.Tensor)
        assert feat.device == style_model.device

def test_fast_style_forward(fast_style_model):
    """Test fast style model forward pass."""
    batch_size = 1
    channels = 3
    height = 256
    width = 256
    
    x = torch.randn(batch_size, channels, height, width)
    x = x.to(fast_style_model.device)
    
    output = fast_style_model(x)
    assert isinstance(output, torch.Tensor)
    assert output.shape == (batch_size, channels, height, width)
    assert output.device == fast_style_model.device

def test_model_devices():
    """Test model device handling."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = StyleTransferModel()
    assert str(model.device) == device
    assert next(model.parameters()).device.type == device

def test_layer_shapes():
    """Test layer output shapes."""
    model = FastStyleTransfer()
    x = torch.randn(1, 3, 256, 256).to(model.device)
    
    # Test initial convolution
    y = model.conv1(x)
    assert y.shape == (1, 32, 256, 256)
    
    # Test residual block
    res_in = torch.randn(1, 32, 256, 256).to(model.device)
    res_out = model.res1(res_in)
    assert res_out.shape == res_in.shape
    
    # Test upsampling
    up_in = torch.randn(1, 32, 256, 256).to(model.device)
    up_out = model.deconv1(up_in)
    assert up_out.shape == (1, 16, 512, 512)
