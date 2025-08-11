"""OCR Engine for processing images and extracting text."""

from PIL import Image
import torch
from transformers import AutoTokenizer, AutoProcessor, AutoModelForImageTextToText
from typing import Union, Optional
import logging

from .config import Config

logger = logging.getLogger(__name__)


class OCREngine:
    """OCR Engine using Nanonets model for text extraction from images."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the OCR engine with given configuration.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
        self.model = None
        self.tokenizer = None
        self.processor = None
        self._load_model()
    
    def _load_model(self):
        """Load the OCR model, tokenizer, and processor."""
        try:
            logger.info(f"Loading model: {self.config.model_path}")
            
            self.model = AutoModelForImageTextToText.from_pretrained(
                self.config.model_path,
                torch_dtype=self.config.torch_dtype,
                device_map=self.config.device_map,
            )
            self.model.eval()
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
            self.processor = AutoProcessor.from_pretrained(self.config.model_path)
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def load_and_resize_image(self, image_input: Union[str, Image.Image]) -> Image.Image:
        """Load and resize an image.
        
        Args:
            image_input: Either a file path string or PIL Image object
            
        Returns:
            Resized PIL Image in RGB format
        """
        if isinstance(image_input, str):
            img = Image.open(image_input).convert("RGB")
        elif isinstance(image_input, Image.Image):
            img = image_input.convert("RGB")
        else:
            raise ValueError("image_input must be either a file path or PIL Image")
        
        w, h = img.size
        max_side = max(w, h)
        
        if max_side > self.config.max_image_side:
            scale = self.config.max_image_side / max_side
            new_w, new_h = int(w * scale), int(h * scale)
            img = img.resize((new_w, new_h), Image.BICUBIC)
            logger.debug(f"Resized image from {w}x{h} to {new_w}x{new_h}")
        
        return img
    
    def extract_text(self, image_input: Union[str, Image.Image]) -> str:
        """Extract text from an image using OCR.
        
        Args:
            image_input: Either a file path string or PIL Image object
            
        Returns:
            Extracted text as string
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call _load_model() first.")
        
        image = self.load_and_resize_image(image_input)
        
        # Prepare the chat template
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": self.config.ocr_prompt},
            ]},
        ]
        
        # Apply chat template and prepare inputs
        text = self.processor.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        inputs = self.processor(
            text=[text], 
            images=[image], 
            padding=True, 
            return_tensors="pt"
        ).to(self.model.device)
        
        # Generate text
        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=self.config.max_new_tokens,
                do_sample=self.config.do_sample,
                temperature=self.config.temperature,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode the generated text
        input_len = inputs.input_ids.shape[1]
        gen_only = output[:, input_len:]
        extracted_text = self.processor.batch_decode(
            gen_only, 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=True
        )[0]
        
        return extracted_text
