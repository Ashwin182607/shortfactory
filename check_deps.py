#!/usr/bin/env python3
"""
Dependency checker for ShortFactory.
Verifies all required dependencies are installed and working.
"""

import importlib
import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from rich.console import Console
from rich.table import Table

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

REQUIRED_PACKAGES = {
    "Core": [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("gradio", "Gradio"),
        ("moviepy", "MoviePy"),
    ],
    "Image": [
        ("PIL", "Pillow"),
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("imageio", "ImageIO"),
    ],
    "Audio": [
        ("soundfile", "SoundFile"),
        ("librosa", "Librosa"),
        ("audioread", "AudioRead"),
    ],
    "Text": [
        ("nltk", "NLTK"),
        ("spacy", "spaCy"),
    ],
    "Utils": [
        ("tqdm", "TQDM"),
        ("requests", "Requests"),
        ("magic", "Python-Magic"),
        ("ffmpeg", "FFMPEG-Python"),
        ("diskcache", "DiskCache"),
        ("tenacity", "Tenacity"),
        ("yaml", "PyYAML"),
    ],
}

def check_package(package: Tuple[str, str]) -> bool:
    """Check if a package is installed and can be imported."""
    module_name, display_name = package
    try:
        importlib.import_module(module_name)
        return True
    except ImportError as e:
        logger.debug(f"Failed to import {display_name}: {e}")
        return False

def main():
    """Run dependency checks and display results."""
    table = Table(title="ShortFactory Dependency Check")
    table.add_column("Category", style="cyan")
    table.add_column("Package", style="magenta")
    table.add_column("Status", style="green")

    all_passed = True
    for category, packages in REQUIRED_PACKAGES.items():
        for package in packages:
            status = "✅ OK" if check_package(package) else "❌ Missing"
            if "Missing" in status:
                all_passed = False
            table.add_row(category, package[1], status)

    console.print(table)

    if not all_passed:
        console.print("\n[red]Some dependencies are missing![/red]")
        console.print("Please install missing packages using:")
        console.print("[yellow]pip install -r requirements.txt[/yellow]")
        sys.exit(1)
    else:
        console.print("\n[green]All dependencies are installed and working![/green]")

if __name__ == "__main__":
    main()
