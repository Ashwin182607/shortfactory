#!/usr/bin/env python3
"""
Launch script for ShortFactory
"""
import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
console = Console()

def setup_environment() -> bool:
    """Set up the Python environment."""
    # Add project root to Python path
    project_root = Path(__file__).parent
    sys.path.append(str(project_root))
    
    # Load environment variables
    load_dotenv()
    return True

def check_dependencies() -> bool:
    """Check for required dependencies."""
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Checking dependencies...", total=7)
            
            # Core dependencies
            import torch
            progress.advance(task)
            import transformers
            progress.advance(task)
            import gradio
            progress.advance(task)
            import moviepy
            progress.advance(task)
            
            # Image processing
            import PIL
            progress.advance(task)
            import cv2
            progress.advance(task)
            import numpy
            progress.advance(task)
            
        console.print("[green]✓[/green] All core dependencies found")
        return True
    except ImportError as e:
        console.print(f"[red]✗[/red] Missing dependency: {str(e)}")
        
        # Try to install dependencies
        console.print("\nInstalling dependencies...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        
        # Verify installation
        try:
            import torch, transformers, gradio, moviepy
            console.print("[green]✓[/green] Dependencies installed successfully")
            return True
        except ImportError:
            console.print("[red]✗[/red] Failed to install dependencies")
            return False

def check_api_keys() -> Dict[str, bool]:
    """Check for required API keys."""
    required_keys = {
        "PEXELS_API_KEY": "Pexels API (image/video assets)",
        "PIXABAY_API_KEY": "Pixabay API (image/video assets)",
        "UNSPLASH_API_KEY": "Unsplash API (image assets)",
    }
    
    status = {}
    for key, description in required_keys.items():
        value = os.getenv(key)
        status[key] = bool(value)
        status_symbol = "[green]✓[/green]" if value else "[yellow]![/yellow]"
        console.print(f"{status_symbol} {description}")
    
    if not all(status.values()):
        console.print("\n[yellow]Note:[/yellow] Some API keys are missing. Limited functionality available.")
    
    return status

def check_directories() -> Dict[str, bool]:
    """Check and create required directories."""
    required_dirs = {
        "assets/videos": "Video assets",
        "assets/music": "Music assets",
        "assets/images": "Image assets",
        "models": "Model weights",
        ".cache": "Cache directory",
        "output": "Output directory",
        "logs": "Log files",
    }
    
    status = {}
    for dir_path, description in required_dirs.items():
        path = Path(dir_path)
        try:
            path.mkdir(parents=True, exist_ok=True)
            status[dir_path] = True
            console.print(f"[green]✓[/green] {description} directory ready")
        except Exception as e:
            status[dir_path] = False
            console.print(f"[red]✗[/red] Failed to create {description} directory: {e}")
    
    return status

def main():
    """Main entry point."""
    console.print(Panel.fit(
        "[bold blue]ShortFactory[/bold blue] - AI Video Content Generation",
        subtitle="[italic]Initializing...[/italic]"
    ))
    
    # Setup checks
    checks = [
        ("Environment", setup_environment()),
        ("Dependencies", check_dependencies()),
        ("Directories", all(check_directories().values())),
        ("API Keys", any(check_api_keys().values())),  # Only need some APIs to work
    ]
    
    # Print setup summary
    console.print("\n[bold]Setup Summary:[/bold]")
    all_passed = True
    for name, passed in checks:
        status = "[green]✓[/green]" if passed else "[red]✗[/red]"
        console.print(f"{status} {name}")
        all_passed = all_passed and passed
    
    if all_passed:
        console.print("\n[green]ShortFactory is ready![/green]")
        
        # Import and run the app
        try:
            from gui.main_ui import ShortFactoryUI
            logger.info(" Web interface loaded")
        except ImportError as e:
            logger.error(f"Failed to load web interface: {str(e)}")
            sys.exit(1)
        
        # Launch web interface
        try:
            # Load environment variables
            load_dotenv()
            
            # Create necessary directories
            os.makedirs('assets/previews', exist_ok=True)
            
            # Check for API keys
            pexels_key = os.getenv('PEXELS_API_KEY')
            pixabay_key = os.getenv('PIXABAY_API_KEY')
            
            if not pexels_key or not pixabay_key:
                logger.warning(
                    "API keys not found in .env file. "
                    "You'll need to add them in the Settings tab."
                )
            
            # Initialize and launch UI
            logger.info("Starting ShortFactory...")
            ui = ShortFactoryUI()
            
            # Launch with Gradio
            ui.launch(
                server_name="0.0.0.0",  # Allow external access
                server_port=7860,  # Default Gradio port
                share=True,  # Create public link
                auth=None,  # No authentication required
                inbrowser=True  # Open in browser automatically
            )
        except Exception as e:
            logger.error(f"Failed to start web interface: {str(e)}")
            sys.exit(1)
    else:
        console.print("\n[red]Setup failed. Please fix the issues above.[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
