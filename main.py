#!/usr/bin/env python3
"""
Main entry point for PDF Information Extraction.

This script provides a command-line interface for extracting text, tables,
equations, and other elements from PDF documents.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from src.pdf_extractor import OCREngine, PDFProcessor, Config
from src.pdf_extractor.utils import setup_logging, save_results, load_config, validate_file_path


def process_pdf(pdf_path: str, config: Config, output_path: Optional[str] = None) -> None:
    """Process a PDF file and extract information.
    
    Args:
        pdf_path: Path to the PDF file
        config: Configuration object
        output_path: Optional path to save results
    """
    # Initialize processors
    pdf_processor = PDFProcessor(config)
    ocr_engine = OCREngine(config)
    
    results = []
    
    try:
        # Process each page
        for page_num, image in enumerate(pdf_processor.pdf_to_images(pdf_path), 1):
            logging.info(f"Processing page {page_num}")
            
            try:
                extracted_text = ocr_engine.extract_text(image)
                
                result = {
                    'page': page_num,
                    'text': extracted_text,
                    'status': 'success'
                }
                
                print(f"\n--- Page {page_num} ---")
                print(extracted_text)
                print(f"--- End Page {page_num} ---\n")
                
            except Exception as e:
                logging.error(f"Failed to process page {page_num}: {e}")
                result = {
                    'page': page_num,
                    'text': '',
                    'status': 'error',
                    'error': str(e)
                }
            
            results.append(result)
    
    except Exception as e:
        logging.error(f"Failed to process PDF: {e}")
        sys.exit(1)
    
    # Save results if output path is provided
    if output_path:
        save_results(results, output_path)


def process_image(image_path: str, config: Config) -> None:
    """Process a single image file.
    
    Args:
        image_path: Path to the image file
        config: Configuration object
    """
    ocr_engine = OCREngine(config)
    
    try:
        extracted_text = ocr_engine.extract_text(image_path)
        print(f"\n--- Extracted Text ---")
        print(extracted_text)
        print(f"--- End ---\n")
        
    except Exception as e:
        logging.error(f"Failed to process image: {e}")
        sys.exit(1)


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extract information from PDF documents using OCR"
    )
    
    parser.add_argument(
        "input_file",
        help="Path to PDF or image file to process"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output path for results (JSON format)"
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--log-level",
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help="Set the logging level"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else args.log_level
    setup_logging(log_level)
    
    # Load configuration
    config = load_config(args.config)
    logging.info(f"Using configuration: {config.model_path}")
    
    # Validate input file
    input_path = args.input_file
    
    if not Path(input_path).exists():
        logging.error(f"Input file not found: {input_path}")
        sys.exit(1)
    
    # Process based on file type
    file_extension = Path(input_path).suffix.lower()
    
    if file_extension == '.pdf':
        if not validate_file_path(input_path, ['.pdf']):
            logging.error(f"Invalid PDF file: {input_path}")
            sys.exit(1)
        
        logging.info(f"Processing PDF file: {input_path}")
        process_pdf(input_path, config, args.output)
        
    elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        if not validate_file_path(input_path, ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']):
            logging.error(f"Invalid image file: {input_path}")
            sys.exit(1)
        
        logging.info(f"Processing image file: {input_path}")
        process_image(input_path, config)
        
    else:
        logging.error(f"Unsupported file type: {file_extension}")
        logging.info("Supported formats: PDF, JPG, JPEG, PNG, BMP, TIFF")
        sys.exit(1)


if __name__ == "__main__":
    main()