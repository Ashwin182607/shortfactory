"""
PyTest configuration and shared fixtures.
"""
import os
import pytest
from pathlib import Path
import shutil
import tempfile

@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="session")
def assets_dir(temp_dir):
    """Create a temporary assets directory."""
    assets_dir = Path(temp_dir) / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    return assets_dir

@pytest.fixture(scope="session")
def models_dir(temp_dir):
    """Create a temporary models directory."""
    models_dir = Path(temp_dir) / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir

@pytest.fixture(scope="session")
def cache_dir(temp_dir):
    """Create a temporary cache directory."""
    cache_dir = Path(temp_dir) / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

@pytest.fixture(scope="session")
def output_dir(temp_dir):
    """Create a temporary output directory."""
    output_dir = Path(temp_dir) / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

@pytest.fixture(scope="session")
def test_env(temp_dir):
    """Set up test environment variables."""
    old_env = dict(os.environ)
    os.environ.update({
        "SHORTFACTORY_ROOT": str(temp_dir),
        "PEXELS_API_KEY": "test_key",
        "PIXABAY_API_KEY": "test_key",
        "UNSPLASH_API_KEY": "test_key"
    })
    yield
    os.environ.clear()
    os.environ.update(old_env)
