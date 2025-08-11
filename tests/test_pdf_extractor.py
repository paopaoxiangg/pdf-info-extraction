"""
Unit tests for the PDF extractor package.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import tempfile
import os

from src.pdf_extractor import OCREngine, PDFProcessor, Config
from src.pdf_extractor.utils import validate_file_path, setup_logging


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        self.assertEqual(config.model_path, "nanonets/Nanonets-OCR-s")
        self.assertEqual(config.max_image_side, 2560)
        self.assertEqual(config.dpi, 300)
        self.assertEqual(config.max_new_tokens, 1536)
        self.assertFalse(config.do_sample)
    
    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        config_dict = {
            'model_path': 'custom/model',
            'max_image_side': 1920,
            'dpi': 200
        }
        config = Config.from_dict(config_dict)
        self.assertEqual(config.model_path, 'custom/model')
        self.assertEqual(config.max_image_side, 1920)
        self.assertEqual(config.dpi, 200)
    
    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = Config()
        config_dict = config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertIn('model_path', config_dict)
        self.assertIn('max_image_side', config_dict)


class TestPDFProcessor(unittest.TestCase):
    """Test cases for PDFProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = Config()
        self.processor = PDFProcessor(self.config)
    
    @patch('fitz.open')
    def test_pdf_to_images(self, mock_fitz_open):
        """Test PDF to images conversion."""
        # Mock PyMuPDF objects
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_pix = MagicMock()
        
        mock_fitz_open.return_value = mock_doc
        mock_doc.__iter__ = Mock(return_value=iter([mock_page]))
        mock_doc.__len__ = Mock(return_value=1)
        
        mock_page.get_pixmap.return_value = mock_pix
        mock_pix.width = 100
        mock_pix.height = 100
        mock_pix.samples = b'\x00' * (100 * 100 * 3)  # RGB data
        
        # Test the method
        images = list(self.processor.pdf_to_images("test.pdf"))
        
        self.assertEqual(len(images), 1)
        self.assertIsInstance(images[0], Image.Image)
        mock_fitz_open.assert_called_once_with("test.pdf")
    
    @patch('fitz.open')
    def test_extract_page_count(self, mock_fitz_open):
        """Test page count extraction."""
        mock_doc = MagicMock()
        mock_fitz_open.return_value = mock_doc
        mock_doc.__len__ = Mock(return_value=5)
        
        page_count = self.processor.extract_page_count("test.pdf")
        
        self.assertEqual(page_count, 5)
        mock_fitz_open.assert_called_once_with("test.pdf")


class TestOCREngine(unittest.TestCase):
    """Test cases for OCREngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = Config()
    
    @patch('src.pdf_extractor.ocr_engine.AutoModelForImageTextToText')
    @patch('src.pdf_extractor.ocr_engine.AutoTokenizer')
    @patch('src.pdf_extractor.ocr_engine.AutoProcessor')
    def test_ocr_engine_init(self, mock_processor, mock_tokenizer, mock_model):
        """Test OCR engine initialization."""
        # Mock the model components
        mock_model.from_pretrained.return_value = MagicMock()
        mock_tokenizer.from_pretrained.return_value = MagicMock()
        mock_processor.from_pretrained.return_value = MagicMock()
        
        engine = OCREngine(self.config)
        
        self.assertIsNotNone(engine.model)
        self.assertIsNotNone(engine.tokenizer)
        self.assertIsNotNone(engine.processor)
    
    def test_load_and_resize_image(self):
        """Test image loading and resizing."""
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            # Create a small test image
            test_img = Image.new('RGB', (100, 100), color='red')
            test_img.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            # Mock the OCR engine (without loading the actual model)
            with patch.object(OCREngine, '_load_model'):
                engine = OCREngine(self.config)
                
                # Test with file path
                img = engine.load_and_resize_image(tmp_path)
                self.assertIsInstance(img, Image.Image)
                self.assertEqual(img.mode, 'RGB')
                
                # Test with PIL Image
                test_img = Image.new('RGB', (50, 50), color='blue')
                img = engine.load_and_resize_image(test_img)
                self.assertIsInstance(img, Image.Image)
                self.assertEqual(img.mode, 'RGB')
        
        finally:
            # Clean up
            os.unlink(tmp_path)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_file_path(self):
        """Test file path validation."""
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
            pdf_path = tmp_pdf.name
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_jpg:
            jpg_path = tmp_jpg.name
        
        try:
            # Test valid files
            self.assertTrue(validate_file_path(pdf_path, ['.pdf']))
            self.assertTrue(validate_file_path(jpg_path, ['.jpg', '.jpeg']))
            
            # Test invalid extension
            self.assertFalse(validate_file_path(pdf_path, ['.jpg']))
            
            # Test non-existent file
            self.assertFalse(validate_file_path('non_existent.pdf', ['.pdf']))
        
        finally:
            # Clean up
            os.unlink(pdf_path)
            os.unlink(jpg_path)
    
    def test_setup_logging(self):
        """Test logging setup."""
        # This should not raise an exception
        setup_logging("INFO")
        setup_logging("DEBUG")


if __name__ == '__main__':
    unittest.main()
