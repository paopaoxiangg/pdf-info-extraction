# PDF Information Extraction

This project uses a powerful OCR model to extract information from PDF documents, including text, tables, and equations.

## Description

This script leverages the `nanonets/Nanonets-OCR-s` model from Hugging Face to perform Optical Character Recognition (OCR) on individual pages of a PDF document (provided as images). It is designed to extract various types of content and format them appropriately:

-   **Text:** Extracts plain text from the document.
-   **Tables:** Converts tables into HTML format.
-   **Equations:** Represents mathematical equations in LaTeX format.
-   **Special Elements:**
    -   **Watermarks:** Wraps watermarks in `<watermark>` tags.
    -   **Page Numbers:** Wraps page numbers in `<page_number>` tags.
    -   **Checkboxes:** Uses ☐ and ☑ for check boxes.
    -   **Images:** Adds a description or caption within `<img>` tags.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/paopaoxiangg/pdf-info-extraction.git
    cd pdf-info-extraction
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Update the image path:**

    Open the `extractpdfleh.py` file and modify the `image_path` variable to point to the image file you want to process:

    ```python
    image_path = "/path/to/your/document.jpg"
    ```

2.  **Run the script:**
    ```bash
    python extractpdfleh.py
    ```

    The script will process the image and print the extracted content to the console.

## Dependencies

This project relies on the following major Python libraries:

-   `torch`
-   `transformers`
-   `Pillow`
-   `accelerate`
-   `huggingface-hub`

A complete list of dependencies can be found in the `requirements.txt` file.
