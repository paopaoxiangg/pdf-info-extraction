from PIL import Image
import torch
from transformers import AutoTokenizer, AutoProcessor, AutoModelForImageTextToText

MODEL_PATH = "nanonets/Nanonets-OCR-s"

model = AutoModelForImageTextToText.from_pretrained(
    MODEL_PATH,
    torch_dtype="auto",
    device_map="auto",           # falls back to CPU if no GPU
    # attn_implementation="flash_attention_2",  # enable only if your GPU/torch supports it
)
model.eval()

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
processor = AutoProcessor.from_pretrained(MODEL_PATH)

PROMPT = (
    "Extract the text from the above document as if you were reading it naturally. "
    "Return the tables in HTML format. Return equations in LaTeX. "
    "If an image lacks a caption, add a brief description inside <img></img>; "
    "otherwise put the caption there. Wrap watermarks as <watermark>...</watermark> "
    "and page numbers as <page_number>...</page_number>. "
    "Prefer using ☐ and ☑ for check boxes."
)

def load_rgb(image_path: str, max_side: int = 2560) -> Image.Image:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    m = max(w, h)
    if m > max_side:
        scale = max_side / m
        img = img.resize((int(w*scale), int(h*scale)), Image.BICUBIC)
    return img

def ocr_page_with_nanonets_s(image_path, model, processor, max_new_tokens=1536):
    image = load_rgb(image_path)

    # Option A: chat template (your approach)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": [
            {"type": "image", "image": image},     # pass PIL image directly
            {"type": "text", "text": PROMPT},
        ]},
    ]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], images=[image], padding=True, return_tensors="pt").to(model.device)

    with torch.inference_mode():
        # If on CUDA, you can also use autocast for speed:
        # with torch.cuda.amp.autocast(dtype=torch.bfloat16):
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=0.0,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Slice off the prompt tokens
    input_len = inputs.input_ids.shape[1]
    gen_only = output[:, input_len:]
    out_text = processor.batch_decode(gen_only, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]
    return out_text

if __name__ == "__main__":
    image_path = "/path/to/your/document.jpg"
    result = ocr_page_with_nanonets_s(image_path, model, processor, max_new_tokens=1536)
    print(result)
