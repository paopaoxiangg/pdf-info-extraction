# PDF Information Extraction

A robust Python package for extracting text, tables, equations, and other elements from PDF documents using advanced OCR models.

## Features

This package leverages the `nanonets/Nanonets-OCR-s` model from Hugging Face to perform Optical Character Recognition (OCR) on PDF documents and images. It is designed to extract various types of content and format them appropriately:

- **Text:** Extracts plain text from documents
- **Tables:** Converts tables into HTML format
- **Equations:** Represents mathematical equations in LaTeX format
- **Special Elements:**
  - **Watermarks:** Wraps watermarks in `<watermark>` tags
  - **Page Numbers:** Wraps page numbers in `<page_number>` tags
  - **Checkboxes:** Uses ☐ and ☑ for check boxes
  - **Images:** Adds descriptions or captions within `<img>` tags

## Project Structure

```
pdf-info-extraction/
├── src/
│   └── pdf_extractor/
│       ├── __init__.py          # Package initialization
│       ├── config.py            # Configuration management
│       ├── ocr_engine.py        # OCR processing engine
│       ├── pdf_processor.py     # PDF to image conversion
│       └── utils.py             # Utility functions
├── config/
│   └── default.json             # Default configuration
├── examples/
│   ├── basic_usage.py           # Basic usage example
│   ├── image_processing.py      # Single image processing
│   └── custom_config.py         # Custom configuration example
├── tests/
│   └── test_pdf_extractor.py    # Unit tests
├── main.py                      # Main CLI script
├── setup.py                     # Package setup
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Installation

### Method 1: Development Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/paopaoxiangg/pdf-info-extraction.git
   cd pdf-info-extraction
   ```

2. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

### Method 2: Direct Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The package provides a convenient command-line interface:

```bash
# Process a PDF file
python main.py document.pdf

# Process a single image
python main.py document.jpg

# Save results to JSON file
python main.py document.pdf -o results.json

# Use custom configuration
python main.py document.pdf -c config/custom.json

# Enable verbose logging
python main.py document.pdf -v
```

### Python API

#### Basic Usage

```python
from src.pdf_extractor import OCREngine, PDFProcessor, Config

# Initialize with default configuration
config = Config()
pdf_processor = PDFProcessor(config)
ocr_engine = OCREngine(config)

# Process a PDF
for page_num, image in enumerate(pdf_processor.pdf_to_images("document.pdf"), 1):
    extracted_text = ocr_engine.extract_text(image)
    print(f"Page {page_num}: {extracted_text}")
```

#### Custom Configuration

```python
from src.pdf_extractor import Config, OCREngine

# Create custom configuration
config = Config(
    max_image_side=1920,
    dpi=200,
    max_new_tokens=1024
)

# Use custom configuration
ocr_engine = OCREngine(config)
text = ocr_engine.extract_text("image.jpg")
```

#### Processing Single Images

```python
from src.pdf_extractor import OCREngine

ocr_engine = OCREngine()
extracted_text = ocr_engine.extract_text("document_page.jpg")
print(extracted_text)
```

### Configuration Options

The package supports various configuration options:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `model_path` | `"nanonets/Nanonets-OCR-s"` | HuggingFace model path |
| `max_image_side` | `2560` | Maximum image side length (pixels) |
| `dpi` | `300` | DPI for PDF to image conversion |
| `max_new_tokens` | `1536` | Maximum tokens for text generation |
| `temperature` | `0.0` | Temperature for text generation |
| `ocr_prompt` | Default prompt | Custom OCR extraction prompt |

### Examples

See the `examples/` directory for more detailed usage examples:

- `basic_usage.py` - Basic PDF processing
- `image_processing.py` - Single image processing
- `custom_config.py` - Using custom configurations

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Or run individual test files:

```bash
python -m unittest tests.test_pdf_extractor
```

## Dependencies

This project relies on the following major Python libraries:

- `torch` - PyTorch for deep learning
- `transformers` - Hugging Face transformers library
- `Pillow` - Python Imaging Library
- `PyMuPDF` - PDF processing
- `accelerate` - Hugging Face acceleration library

A complete list of dependencies can be found in the `requirements.txt` file.
