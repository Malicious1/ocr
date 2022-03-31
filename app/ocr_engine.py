from typing import List
import cv2
import numpy as np
from PIL import Image
import string
import simplemma

from app.language import AvailableLanguages, Language
from app.ocr_backend import OCRBackend, TesseractBackend

# TODO: image preprocessing must go to OCR backend


class OCREngine:

    def __init__(self, ocr_backend: OCRBackend = None):
        self._available_languages = AvailableLanguages()
        self._lang_data = simplemma.load_data(*self._available_languages.langs_abbr_2)
        self._ocr_backend = TesseractBackend() if ocr_backend is None else ocr_backend
        
    @property
    def available_languages(self) -> AvailableLanguages:
        return self._available_languages

    @property
    def ocr_backend(self) -> OCRBackend:
        return self._ocr_backend

    def get_text(self, image: Image, languages: List[Language]) -> str:
        image = self.preprocess_image(image)
        text = self.ocr_backend.get_text(image, languages)
        text = self.postprocess_text(text)
        return text

    @staticmethod
    def preprocess_image(image: Image):
        image = np.array(image)
        # image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        # image = cv2.bilateralFilter(image, 7, 55, 60)
        # _, image = cv2.threshold(src=image, thresh=70, maxval=255, type=cv2.THRESH_BINARY)
        image = Image.fromarray(image)
        return image

    def postprocess_text(self, text: str):
        text = text.replace('\n', ' ')
        text = text.strip()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = " ".join([simplemma.lemmatize(x, self._lang_data) for x in text.split(' ') if len(x)])
        return text
