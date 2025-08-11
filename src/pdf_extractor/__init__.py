"""
PDF Information Extraction Package

A Python package for extracting text, tables, equations, and other elements 
from PDF documents using advanced OCR models.
"""

from .ocr_engine import OCREngine
from .pdf_processor import PDFProcessor
from .config import Config

__version__ = "1.0.0"
__author__ = "paopaoxiangg"

__all__ = ['OCREngine', 'PDFProcessor', 'Config']
