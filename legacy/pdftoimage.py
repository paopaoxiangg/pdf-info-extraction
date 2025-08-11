import fitz  # PyMuPDF
from PIL import Image
import numpy as np

def pdf_pages_as_pil_pymupdf(pdf_path, dpi=400):
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    for page in doc:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        yield img
    doc.close()

# usage with your function
for i, img in enumerate(pdf_pages_as_pil_pymupdf("doc.pdf", dpi=300), 1):
    text = ocr_page_with_nanonets_s(img, model, processor)  # pass PIL Image
