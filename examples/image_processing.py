#!/usr/bin/env python3
"""
Example: Single image processing

This example demonstrates how to process a single image file
using the OCR engine.
"""

from PIL import Image
from src.pdf_extractor import OCREngine, Config
from src.pdf_extractor.utils import setup_logging


def main():
    # Setup logging
    setup_logging("INFO")
    
    # Create configuration
    config = Config()
    
    # Initialize OCR engine
    ocr_engine = OCREngine(config)
    
    # Example image path (update this to your actual image)
    image_path = "example_document.jpg"
    
    try:
        print(f"Processing image: {image_path}")
        
        # Extract text from the image
        extracted_text = ocr_engine.extract_text(image_path)
        
        print("\n--- Extracted Text ---")
        print(extracted_text)
        print("--- End ---\n")
        
    except FileNotFoundError:
        print(f"Image file not found: {image_path}")
        print("Please place your image file in the current directory.")
    except Exception as e:
        print(f"Error processing image: {e}")


if __name__ == "__main__":
    main()
