"""
Logging utilities for ShortFactory.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Setup logging configuration for ShortFactory.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Optional path to log file
        format_string: Optional custom format string
    """
    if format_string is None:
        format_string = '[%(asctime)s] %(levelname)s [%(name)s] %(message)s'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(str(log_file)))
    
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=handlers
    )
    
    # Suppress some noisy loggers
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)
