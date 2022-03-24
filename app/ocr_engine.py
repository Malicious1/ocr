import pytesseract
from typing import List
import cv2
import numpy as np
from PIL import Image
import string
import simplemma

from app.language import AvailableLanguages
from app.exceptions import InvalidLanguageError


class OCREngine:

    def __init__(self):
        self._available_languages = AvailableLanguages()
        self._lang_data = simplemma.load_data(*self._available_languages.langs4simplelemma)
        self._validate_languages()
        
    @property
    def available_languages(self) -> List[str]:
        return self._available_languages.langs4tesseract

    def _validate_languages(self):
        # Check if available_languages declaration is a subset of Tesseract available language models
        tesseract_languages = pytesseract.get_languages()
        if not set(self.available_languages).issubset(set(tesseract_languages)):
            raise InvalidLanguageError("Available languages declaration inconsistent with Tesseract models")

    def get_text(self, image: Image, languages: str = None) -> str:
        languages = "+".join(self.available_languages) if languages is None else languages
        if not set(languages.split("+")).issubset(set(self.available_languages)):
            raise InvalidLanguageError(
                "Requested languages not available, available languages: %s", str(self.available_languages))
        image = self.preprocess_image(image)
        text = pytesseract.image_to_string(image=image, lang=languages)
        text = self.postprocess_text(text)
        return text

    @staticmethod
    def preprocess_image(image: Image):
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        image = cv2.bilateralFilter(image, 7, 55, 60)
        _, image = cv2.threshold(src=image, thresh=225, maxval=255, type=cv2.THRESH_BINARY)
        image = Image.fromarray(image)
        return image

    def postprocess_text(self, text: str):
        text = text.replace('\n', ' ')
        text = text.strip()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = " ".join([simplemma.lemmatize(x, self._lang_data) for x in text.split(' ') if len(x)])
        return text
