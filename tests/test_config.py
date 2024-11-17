"""
Tests for configuration management.
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from factory_core.config.validation import ConfigValidator

@pytest.fixture
def config_validator():
    """Create config validator instance."""
    return ConfigValidator()

def test_api_key_validation(config_validator):
    """Test API key validation."""
    with patch.dict(os.environ, {
        'PEXELS_API_KEY': 'test_key',
        'PIXABAY_API_KEY': 'test_key',
        'UNSPLASH_API_KEY': 'test_key'
    }):
        results = ConfigValidator.validate_api_keys()
        assert all(results.values())

def test_directory_validation(config_validator):
    """Test directory validation."""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.mkdir'):
            results = ConfigValidator.validate_directories()
            assert all(results.values())

def test_dependency_validation(config_validator):
    """Test dependency validation."""
    with patch('builtins.__import__', return_value=None):
        results = ConfigValidator.validate_dependencies()
        assert all(results.values())

def test_gpu_validation(config_validator):
    """Test GPU validation."""
    with patch('torch.cuda.is_available', return_value=True):
        with patch('torch.cuda.device_count', return_value=1):
            with patch('torch.cuda.get_device_name', return_value='Test GPU'):
                results = ConfigValidator.validate_gpu()
                assert results['cuda_available']
                assert results['device_count'] == 1
                assert 'Test GPU' in results['device_names']

def test_validation_report(config_validator):
    """Test validation report generation."""
    with patch.multiple(ConfigValidator,
        validate_api_keys=MagicMock(return_value={'test_key': True}),
        validate_directories=MagicMock(return_value={'test_dir': True}),
        validate_dependencies=MagicMock(return_value={'test_dep': True}),
        validate_gpu=MagicMock(return_value={'cuda_available': True})
    ):
        results = ConfigValidator.validate_all()
        assert all(isinstance(v, dict) for v in results.values())
        assert all(results['api_keys'].values())
        assert all(results['directories'].values())
        assert all(results['dependencies'].values())
        assert results['gpu']['cuda_available']
