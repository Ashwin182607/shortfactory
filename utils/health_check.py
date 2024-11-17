"""
System health check utilities.
"""
import os
import psutil
import logging
from typing import Dict, List, Optional, Union
import torch
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

class SystemHealthCheck:
    """System health monitoring for ShortFactory."""
    
    @staticmethod
    def check_memory() -> Dict[str, Union[float, str]]:
        """Check system memory status."""
        memory = psutil.virtual_memory()
        return {
            "total": f"{memory.total / (1024**3):.2f}GB",
            "available": f"{memory.available / (1024**3):.2f}GB",
            "percent_used": memory.percent,
            "warning": memory.percent > 90
        }
    
    @staticmethod
    def check_disk_space() -> Dict[str, Union[float, str]]:
        """Check available disk space."""
        disk = psutil.disk_usage('/')
        return {
            "total": f"{disk.total / (1024**3):.2f}GB",
            "free": f"{disk.free / (1024**3):.2f}GB",
            "percent_used": disk.percent,
            "warning": disk.percent > 90
        }
    
    @staticmethod
    def check_gpu_memory() -> Dict[str, Union[float, str, List]]:
        """Check GPU memory status if available."""
        if not torch.cuda.is_available():
            return {"available": False}
        
        devices = []
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            memory = torch.cuda.memory_stats(i)
            allocated = memory.get('allocated_bytes.all.current', 0) / (1024**3)
            reserved = memory.get('reserved_bytes.all.current', 0) / (1024**3)
            
            devices.append({
                "name": props.name,
                "total_memory": f"{props.total_memory / (1024**3):.2f}GB",
                "allocated": f"{allocated:.2f}GB",
                "reserved": f"{reserved:.2f}GB",
                "warning": allocated / (props.total_memory / (1024**3)) > 0.9
            })
        
        return {
            "available": True,
            "devices": devices
        }
    
    @staticmethod
    def check_cache_size() -> Dict[str, Union[float, str]]:
        """Check cache directory size."""
        cache_dir = Path(".cache")
        if not cache_dir.exists():
            return {"size": "0MB", "warning": False}
        
        total_size = 0
        for path in cache_dir.rglob('*'):
            if path.is_file():
                total_size += path.stat().st_size
        
        size_mb = total_size / (1024**2)
        return {
            "size": f"{size_mb:.2f}MB",
            "warning": size_mb > 1000  # Warning if cache exceeds 1GB
        }
    
    @classmethod
    def run_health_check(cls) -> Dict[str, Dict]:
        """Run all health checks."""
        return {
            "memory": cls.check_memory(),
            "disk": cls.check_disk_space(),
            "gpu": cls.check_gpu_memory(),
            "cache": cls.check_cache_size()
        }
    
    @classmethod
    def print_health_report(cls):
        """Print a formatted health report."""
        results = cls.run_health_check()
        
        print("\n=== ShortFactory Health Report ===\n")
        
        # System Memory
        print("System Memory:")
        memory = results["memory"]
        print(f"  Total: {memory['total']}")
        print(f"  Available: {memory['available']}")
        print(f"  Used: {memory['percent_used']}%")
        if memory["warning"]:
            print("  ⚠️ Warning: High memory usage!")
        
        # Disk Space
        print("\nDisk Space:")
        disk = results["disk"]
        print(f"  Total: {disk['total']}")
        print(f"  Free: {disk['free']}")
        print(f"  Used: {disk['percent_used']}%")
        if disk["warning"]:
            print("  ⚠️ Warning: Low disk space!")
        
        # GPU Status
        print("\nGPU Status:")
        gpu = results["gpu"]
        if gpu["available"]:
            for i, device in enumerate(gpu["devices"]):
                print(f"  Device {i}: {device['name']}")
                print(f"    Total Memory: {device['total_memory']}")
                print(f"    Allocated: {device['allocated']}")
                print(f"    Reserved: {device['reserved']}")
                if device["warning"]:
                    print("    ⚠️ Warning: High GPU memory usage!")
        else:
            print("  No GPU available")
        
        # Cache Status
        print("\nCache Status:")
        cache = results["cache"]
        print(f"  Size: {cache['size']}")
        if cache["warning"]:
            print("  ⚠️ Warning: Large cache size!")
        
        print("\n=== End Report ===\n")
    
    @classmethod
    def clean_cache(cls):
        """Clean the cache directory."""
        cache_dir = Path(".cache")
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
            cache_dir.mkdir()
            logger.info("Cache cleaned successfully")
        else:
            logger.info("No cache directory found")
