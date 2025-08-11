#!/usr/bin/env python3
"""
Example: Basic PDF extraction usage

This example demonstrates how to use the PDF extractor to process a PDF file
and extract text, tables, and other elements.
"""

import logging
from pathlib import Path

from src.pdf_extractor import OCREngine, PDFProcessor, Config
from src.pdf_extractor.utils import setup_logging


def main():
    # Setup logging
    setup_logging("INFO")
    
    # Create configuration
    config = Config()
    
    # Initialize processors
    pdf_processor = PDFProcessor(config)
    ocr_engine = OCREngine(config)
    
    # Example PDF path (update this to your actual PDF)
    pdf_path = "example_document.pdf"
    
    if not Path(pdf_path).exists():
        print(f"Please place your PDF file at: {pdf_path}")
        return
    
    print(f"Processing PDF: {pdf_path}")
    
    # Process each page
    for page_num, image in enumerate(pdf_processor.pdf_to_images(pdf_path), 1):
        print(f"\n--- Processing Page {page_num} ---")
        
        try:
            # Extract text from the page
            extracted_text = ocr_engine.extract_text(image)
            
            print(f"Extracted text from page {page_num}:")
            print(extracted_text)
            print(f"--- End Page {page_num} ---\n")
            
        except Exception as e:
            logging.error(f"Failed to process page {page_num}: {e}")


if __name__ == "__main__":
    main()
