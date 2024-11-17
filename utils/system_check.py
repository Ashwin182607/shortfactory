#!/usr/bin/env python3

import os
import sys
import psutil
import shutil
import platform
from pathlib import Path
from typing import Dict, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.progress import track
import torch
import pkg_resources

console = Console()

class SystemCheck:
    def __init__(self):
        self.console = Console()
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []

    def check_python_version(self) -> bool:
        min_version = (3, 8)
        current = sys.version_info[:2]
        return current >= min_version

    def check_gpu(self) -> Tuple[bool, str]:
        if torch.cuda.is_available():
            return True, f"GPU available: {torch.cuda.get_device_name(0)}"
        return False, "No GPU detected"

    def check_disk_space(self, min_space_gb: float = 10.0) -> bool:
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)
        return free_gb >= min_space_gb

    def check_memory(self, min_memory_gb: float = 4.0) -> bool:
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024 ** 3)
        return total_gb >= min_memory_gb

    def check_dependencies(self) -> List[Tuple[str, bool]]:
        required = pkg_resources.parse_requirements(
            Path("requirements.txt").read_text()
        )
        results = []
        for req in required:
            try:
                pkg_resources.require(str(req))
                results.append((str(req), True))
            except (pkg_resources.DistributionNotFound, 
                   pkg_resources.VersionConflict):
                results.append((str(req), False))
        return results

    def check_directories(self) -> Dict[str, bool]:
        dirs = {
            "assets": Path("assets"),
            "models": Path("models"),
            "output": Path("output"),
            "logs": Path("logs"),
            "cache": Path(".cache")
        }
        return {name: path.exists() for name, path in dirs.items()}

    def check_env_file(self) -> bool:
        return Path(".env").exists()

    def run_all_checks(self):
        with self.console.status("[bold green]Running system checks..."):
            # Python Version
            python_ok = self.check_python_version()
            self.console.print(f"Python version: {'✓' if python_ok else '✗'} {sys.version}")
            
            # GPU Check
            gpu_ok, gpu_info = self.check_gpu()
            self.console.print(f"GPU status: {'✓' if gpu_ok else '-'} {gpu_info}")
            
            # System Resources
            disk_ok = self.check_disk_space()
            memory_ok = self.check_memory()
            self.console.print(f"Disk space: {'✓' if disk_ok else '✗'}")
            self.console.print(f"Memory: {'✓' if memory_ok else '✗'}")
            
            # Dependencies
            deps_table = Table(title="Dependencies")
            deps_table.add_column("Package")
            deps_table.add_column("Status")
            
            dep_results = self.check_dependencies()
            for dep, ok in dep_results:
                deps_table.add_row(
                    dep, 
                    "[green]✓" if ok else "[red]✗"
                )
            self.console.print(deps_table)
            
            # Directories
            dir_results = self.check_directories()
            dir_table = Table(title="Directories")
            dir_table.add_column("Directory")
            dir_table.add_column("Status")
            
            for dir_name, exists in dir_results.items():
                dir_table.add_row(
                    dir_name,
                    "[green]✓" if exists else "[yellow]missing"
                )
            self.console.print(dir_table)
            
            # Environment
            env_ok = self.check_env_file()
            self.console.print(f"Environment file: {'✓' if env_ok else '✗'}")

def main():
    checker = SystemCheck()
    checker.run_all_checks()

if __name__ == "__main__":
    main()
