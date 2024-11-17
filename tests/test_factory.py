"""
Tests for ShortFactory core functionality.
"""
import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from factory_core.factory import ShortFactory, VideoConfig
from factory_core.ai.style_manager import StyleType

@pytest.fixture
def factory():
    """Create a ShortFactory instance for testing."""
    return ShortFactory()

@pytest.fixture
def video_config():
    """Create a basic video configuration."""
    return VideoConfig(
        topic="Test video",
        duration=30,
        style=StyleType.MINIMAL
    )

def test_factory_initialization(factory):
    """Test factory initialization."""
    assert factory is not None
    assert factory.model_manager is not None
    assert factory.style_manager is not None
    assert factory.asset_manager is not None
    assert factory.audio_manager is not None
    assert factory.video_editor is not None

def test_script_generation(factory, video_config):
    """Test script generation."""
    with patch('factory_core.ai.script_generator.ScriptGenerator.generate_script') as mock_generate:
        mock_generate.return_value = "Test script content"
        script = factory._generate_script(video_config)
        assert script == "Test script content"
        mock_generate.assert_called_once()

def test_asset_sourcing(factory):
    """Test asset sourcing."""
    with patch('factory_core.assets.asset_manager.AssetManager.get_video') as mock_get_video:
        mock_get_video.return_value = "/path/to/video.mp4"
        video_path = factory.asset_manager.get_video("test query")
        assert video_path == "/path/to/video.mp4"
        mock_get_video.assert_called_once_with("test query")

def test_style_transfer(factory):
    """Test style transfer."""
    with patch('factory_core.ai.style_manager.StyleManager.apply_style') as mock_apply:
        mock_apply.return_value = "/path/to/styled.mp4"
        result = factory.style_manager.apply_style(
            "/path/to/input.mp4",
            StyleType.CINEMATIC
        )
        assert result == "/path/to/styled.mp4"
        mock_apply.assert_called_once()

def test_video_creation_pipeline(factory, video_config):
    """Test the entire video creation pipeline."""
    with patch.multiple(factory,
        _generate_script=MagicMock(return_value="Test script"),
        _source_assets=MagicMock(return_value=["/path/to/video.mp4"]),
        _apply_style=MagicMock(return_value="/path/to/styled.mp4"),
        _generate_audio=MagicMock(return_value="/path/to/audio.wav"),
        _compose_video=MagicMock(return_value="/path/to/final.mp4")
    ):
        output_path = factory.create_video(video_config)
        assert output_path == "/path/to/final.mp4"
        factory._generate_script.assert_called_once()
        factory._source_assets.assert_called_once()
        factory._apply_style.assert_called_once()
        factory._generate_audio.assert_called_once()
        factory._compose_video.assert_called_once()
