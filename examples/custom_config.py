#!/usr/bin/env python3
"""
Example: Custom configuration usage

This example demonstrates how to use custom configurations
for the PDF extraction process.
"""

import json
from src.pdf_extractor import OCREngine, PDFProcessor, Config
from src.pdf_extractor.utils import setup_logging, save_results


def main():
    # Setup logging
    setup_logging("INFO")
    
    # Create custom configuration
    config = Config(
        max_image_side=1920,  # Smaller image size for faster processing
        dpi=200,              # Lower DPI for faster processing
        max_new_tokens=1024,  # Fewer tokens for faster generation
        ocr_prompt="Extract only the main text content from this document."  # Simplified prompt
    )
    
    print("Custom Configuration:")
    print(f"  Max image side: {config.max_image_side}")
    print(f"  DPI: {config.dpi}")
    print(f"  Max new tokens: {config.max_new_tokens}")
    
    # Initialize processors
    pdf_processor = PDFProcessor(config)
    ocr_engine = OCREngine(config)
    
    # Example PDF path
    pdf_path = "example_document.pdf"
    
    results = []
    
    try:
        # Process first 3 pages only
        for page_num, image in enumerate(pdf_processor.pdf_to_images(pdf_path), 1):
            if page_num > 3:  # Limit to first 3 pages
                break
                
            print(f"\nProcessing page {page_num} with custom config...")
            
            extracted_text = ocr_engine.extract_text(image)
            
            result = {
                'page': page_num,
                'text': extracted_text,
                'config_used': config.to_dict()
            }
            results.append(result)
            
            print(f"Page {page_num} processed successfully")
    
    except FileNotFoundError:
        print(f"PDF file not found: {pdf_path}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Save results
    save_results(results, "custom_extraction_results.json")
    print(f"\nProcessed {len(results)} pages and saved results.")


if __name__ == "__main__":
    main()
