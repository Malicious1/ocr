import pytesseract
from typing import List
import cv2
import numpy as np
from PIL import Image


class OCREngine:

    @staticmethod
    def get_text(image: Image, language: str) -> str:
        image = cv2.bilateralFilter(np.asarray(image), 5, 55, 60)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, image = cv2.threshold(image, 240, 255, 1)
        return pytesseract.image_to_string(Image.fromarray(image), lang=language)

    @staticmethod
    def get_languages() -> List[str]:
        return pytesseract.get_languages()
