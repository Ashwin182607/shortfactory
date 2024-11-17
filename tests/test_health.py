"""
Tests for system health monitoring.
"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from utils.health_check import SystemHealthCheck

@pytest.fixture
def health_check():
    """Create health check instance."""
    return SystemHealthCheck()

def test_memory_check(health_check):
    """Test memory status check."""
    mock_memory = MagicMock(
        total=16 * (1024**3),  # 16GB
        available=8 * (1024**3),  # 8GB
        percent=50.0
    )
    
    with patch('psutil.virtual_memory', return_value=mock_memory):
        results = SystemHealthCheck.check_memory()
        assert results['total'] == '16.00GB'
        assert results['available'] == '8.00GB'
        assert results['percent_used'] == 50.0
        assert not results['warning']

def test_disk_check(health_check):
    """Test disk space check."""
    mock_disk = MagicMock(
        total=500 * (1024**3),  # 500GB
        free=250 * (1024**3),   # 250GB
        percent=50.0
    )
    
    with patch('psutil.disk_usage', return_value=mock_disk):
        results = SystemHealthCheck.check_disk_space()
        assert results['total'] == '500.00GB'
        assert results['free'] == '250.00GB'
        assert results['percent_used'] == 50.0
        assert not results['warning']

def test_gpu_check(health_check):
    """Test GPU memory check."""
    with patch('torch.cuda.is_available', return_value=True):
        with patch('torch.cuda.device_count', return_value=1):
            with patch('torch.cuda.get_device_properties') as mock_props:
                with patch('torch.cuda.memory_stats') as mock_stats:
                    mock_props.return_value = MagicMock(
                        name='Test GPU',
                        total_memory=8 * (1024**3)  # 8GB
                    )
                    mock_stats.return_value = {
                        'allocated_bytes.all.current': 2 * (1024**3),  # 2GB
                        'reserved_bytes.all.current': 3 * (1024**3)    # 3GB
                    }
                    
                    results = SystemHealthCheck.check_gpu_memory()
                    assert results['available']
                    assert len(results['devices']) == 1
                    device = results['devices'][0]
                    assert device['name'] == 'Test GPU'
                    assert device['total_memory'] == '8.00GB'
                    assert device['allocated'] == '2.00GB'
                    assert device['reserved'] == '3.00GB'
                    assert not device['warning']

def test_cache_check(health_check):
    """Test cache size check."""
    mock_path = MagicMock()
    mock_path.stat.return_value = MagicMock(st_size=500 * (1024**2))  # 500MB
    
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.rglob', return_value=[mock_path]):
            results = SystemHealthCheck.check_cache_size()
            assert results['size'] == '500.00MB'
            assert not results['warning']

def test_clean_cache(health_check):
    """Test cache cleaning."""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('shutil.rmtree') as mock_rmtree:
            with patch('pathlib.Path.mkdir') as mock_mkdir:
                SystemHealthCheck.clean_cache()
                mock_rmtree.assert_called_once()
                mock_mkdir.assert_called_once()
