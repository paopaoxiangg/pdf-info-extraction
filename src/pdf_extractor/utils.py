"""Utility functions for the PDF extractor package."""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import Config


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def save_results(results: List[Dict[str, Any]], output_path: str) -> None:
    """Save extraction results to a JSON file.
    
    Args:
        results: List of extraction results
        output_path: Path to save the JSON file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logging.info(f"Results saved to {output_path}")


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or return default config.
    
    Args:
        config_path: Path to configuration file (JSON format)
        
    Returns:
        Config object
    """
    if config_path and Path(config_path).exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        return Config.from_dict(config_dict)
    else:
        return Config()


def validate_file_path(file_path: str, extensions: List[str]) -> bool:
    """Validate if file exists and has correct extension.
    
    Args:
        file_path: Path to the file
        extensions: List of allowed file extensions (e.g., ['.pdf', '.jpg'])
        
    Returns:
        True if file is valid, False otherwise
    """
    path = Path(file_path)
    return path.exists() and path.suffix.lower() in [ext.lower() for ext in extensions]
