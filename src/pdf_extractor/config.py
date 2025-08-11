"""Configuration settings for PDF extraction."""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Config:
    """Configuration class for PDF extraction settings."""
    
    # Model settings
    model_path: str = "nanonets/Nanonets-OCR-s"
    device_map: str = "auto"
    torch_dtype: str = "auto"
    
    # Image processing settings
    max_image_side: int = 2560
    dpi: int = 300
    
    # Generation settings
    max_new_tokens: int = 1536
    do_sample: bool = False
    temperature: float = 0.0
    
    # OCR prompt
    ocr_prompt: str = (
        "Extract the text from the above document as if you were reading it naturally. "
        "Return the tables in HTML format. Return equations in LaTeX. "
        "If an image lacks a caption, add a brief description inside <img></img>; "
        "otherwise put the caption there. Wrap watermarks as <watermark>...</watermark> "
        "and page numbers as <page_number>...</page_number>. "
        "Prefer using ☐ and ☑ for check boxes."
    )
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create Config instance from dictionary."""
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Config instance to dictionary."""
        return {
            'model_path': self.model_path,
            'device_map': self.device_map,
            'torch_dtype': self.torch_dtype,
            'max_image_side': self.max_image_side,
            'dpi': self.dpi,
            'max_new_tokens': self.max_new_tokens,
            'do_sample': self.do_sample,
            'temperature': self.temperature,
            'ocr_prompt': self.ocr_prompt
        }
