from pathlib import Path
import json
from app.ocr_engine import *

ABS_PATH_TO_IMAGES = "/code/images" # move to config

def test_ocr():
    with open(Path(ABS_PATH_TO_IMAGES) / 'text.json', 'r') as f:
        test_json = json.load(f)
    image_paths = [k for k,v in list(test_json.items())[:3]]
    for impath in image_paths:
        with Image.open(Path('/code/') / impath) as img:
            res = OCREngine.get_text(img, 'pol+eng')
        assert type(res) == str
