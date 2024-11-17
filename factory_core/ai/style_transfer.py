"""
Style Transfer Models for video style transformation.
"""
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models

logger = logging.getLogger(__name__)

class StyleTransferModel(nn.Module):
    """Neural style transfer model."""
    
    def __init__(self):
        super().__init__()
        # Load VGG19 and freeze parameters
        vgg = models.vgg19(pretrained=True).features
        for param in vgg.parameters():
            param.requires_grad_(False)
        
        # Split VGG into sections
        self.blocks = nn.ModuleList([
            vgg[:4],   # relu1_1
            vgg[4:9],  # relu2_1
            vgg[9:18], # relu3_1
            vgg[18:27],# relu4_1
            vgg[27:36] # relu5_1
        ])
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)
        self.eval()
    
    def forward(self, x: torch.Tensor) -> List[torch.Tensor]:
        """Forward pass through VGG blocks."""
        features = []
        for block in self.blocks:
            x = block(x)
            features.append(x)
        return features

class FastStyleTransfer(nn.Module):
    """Fast neural style transfer model."""
    
    def __init__(self):
        super().__init__()
        # Initial convolution
        self.conv1 = ConvLayer(3, 32, 9, 1)
        self.in1 = nn.InstanceNorm2d(32, affine=True)
        
        # Residual blocks
        self.res1 = ResidualBlock(32)
        self.res2 = ResidualBlock(32)
        self.res3 = ResidualBlock(32)
        self.res4 = ResidualBlock(32)
        self.res5 = ResidualBlock(32)
        
        # Upsampling
        self.deconv1 = UpsampleConvLayer(32, 16, 3, 1, 2)
        self.in4 = nn.InstanceNorm2d(16, affine=True)
        self.deconv2 = UpsampleConvLayer(16, 8, 3, 1, 2)
        self.in5 = nn.InstanceNorm2d(8, affine=True)
        self.deconv3 = ConvLayer(8, 3, 9, 1)
        
        # Initialize weights
        self._initialize_weights()
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        # Initial convolution
        y = F.relu(self.in1(self.conv1(x)))
        
        # Residual blocks
        y = self.res1(y)
        y = self.res2(y)
        y = self.res3(y)
        y = self.res4(y)
        y = self.res5(y)
        
        # Upsampling
        y = F.relu(self.in4(self.deconv1(y)))
        y = F.relu(self.in5(self.deconv2(y)))
        y = self.deconv3(y)
        
        return y
    
    def _initialize_weights(self):
        """Initialize model weights."""
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.normal_(module.weight.data, 0.0, 0.02)
                if module.bias is not None:
                    module.bias.data.zero_()
            elif isinstance(module, nn.BatchNorm2d):
                nn.init.normal_(module.weight.data, 1.0, 0.02)
                nn.init.constant_(module.bias.data, 0)

class ConvLayer(nn.Module):
    """Custom convolution layer."""
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int, stride: int):
        super().__init__()
        reflection_padding = kernel_size // 2
        self.reflection_pad = nn.ReflectionPad2d(reflection_padding)
        self.conv2d = nn.Conv2d(in_channels, out_channels, kernel_size, stride)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.reflection_pad(x)
        out = self.conv2d(out)
        return out

class ResidualBlock(nn.Module):
    """Residual block for style transfer."""
    def __init__(self, channels: int):
        super().__init__()
        self.conv1 = ConvLayer(channels, channels, 3, 1)
        self.in1 = nn.InstanceNorm2d(channels, affine=True)
        self.conv2 = ConvLayer(channels, channels, 3, 1)
        self.in2 = nn.InstanceNorm2d(channels, affine=True)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        out = F.relu(self.in1(self.conv1(x)))
        out = self.in2(self.conv2(out))
        out = out + residual
        return out

class UpsampleConvLayer(nn.Module):
    """Upsampling convolution layer."""
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int, stride: int, upsample: int = None):
        super().__init__()
        self.upsample = upsample
        reflection_padding = kernel_size // 2
        self.reflection_pad = nn.ReflectionPad2d(reflection_padding)
        self.conv2d = nn.Conv2d(in_channels, out_channels, kernel_size, stride)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.upsample:
            x = F.interpolate(x, scale_factor=self.upsample, mode='nearest')
        out = self.reflection_pad(x)
        out = self.conv2d(out)
        return out
