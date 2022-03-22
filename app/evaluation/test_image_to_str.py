import json
from pathlib import Path

from app.ocr_engine import OCREngine
from app.eval import evaluate_ocr

with open(Path(__file__).parent / 'images/text.json', 'r') as f:
    test_json = json.load(f)

ocr_call = lambda x : OCREngine.get_text(x, "pol+eng+rus+ukr")

scores = evaluate_ocr(ocr_call, test_json, silent = False, image_dir = 'images/')

avg_ = 0
for path, score in scores.items():
    print(f' - {path:40} : {score:.3f}')
    avg_ += score
avg_ = avg_/len(scores)
print(f'Average : {avg_:.3f}')
