import pytesseract
from typing import List
import cv2
import numpy as np
from PIL import Image


class OCREngine:

    @staticmethod
    def get_text(image: Image, language: str) -> str:
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        image = cv2.bilateralFilter(image, 7, 55, 60)
        _, image = cv2.threshold(src=image, thresh=225, maxval=255, type=cv2.THRESH_BINARY)
        image = Image.fromarray(image)
        return pytesseract.image_to_string(image=image, lang=language)

    @staticmethod
    def get_languages() -> List[str]:
        return pytesseract.get_languages()
