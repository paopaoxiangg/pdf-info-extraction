"""PDF processing utilities for converting PDF pages to images."""

import fitz  # PyMuPDF
from PIL import Image
from typing import Iterator, Optional
import logging

from .config import Config

logger = logging.getLogger(__name__)


class PDFProcessor:
    """PDF processing class for converting PDF pages to images."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the PDF processor.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
    
    def pdf_to_images(self, pdf_path: str) -> Iterator[Image.Image]:
        """Convert PDF pages to PIL Images.
        
        Args:
            pdf_path: Path to the PDF file
            
        Yields:
            PIL Image objects for each page
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If PDF cannot be processed
        """
        try:
            doc = fitz.open(pdf_path)
            logger.info(f"Processing PDF: {pdf_path} ({len(doc)} pages)")
            
            zoom = self.config.dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            
            for page_num, page in enumerate(doc, 1):
                try:
                    pix = page.get_pixmap(matrix=mat, alpha=False)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    logger.debug(f"Converted page {page_num} to image ({img.size})")
                    yield img
                except Exception as e:
                    logger.error(f"Failed to convert page {page_num}: {e}")
                    continue
            
            doc.close()
            logger.info("PDF processing completed")
            
        except FileNotFoundError:
            logger.error(f"PDF file not found: {pdf_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to process PDF {pdf_path}: {e}")
            raise
    
    def extract_page_count(self, pdf_path: str) -> int:
        """Get the number of pages in a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages in the PDF
        """
        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            doc.close()
            return page_count
        except Exception as e:
            logger.error(f"Failed to get page count for {pdf_path}: {e}")
            raise
