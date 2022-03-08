import json
from pathlib import Path

from PIL import Image

from app.ocr_engine import OCREngine

ocr_engine = OCREngine()

with open(Path(__file__).parent / 'images/text.json', 'r') as f:
    text_json = json.load(f)

for img_path, text in text_json.items():

    with Image.open(img_path) as img:
        print(ocr_engine.get_text(img, "pol").replace('\n', ' '))
        print(text)
        print('###########')
