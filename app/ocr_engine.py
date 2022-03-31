from typing import List
from PIL import Image
import string
import simplemma

from app.language import AvailableLanguages, Language
from app.ocr_backend import OCRBackend, TesseractBackend


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
        text = self.ocr_backend.get_text(image, languages)
        text = self.postprocess_text(text)
        return text

    def postprocess_text(self, text: str):
        text = text.replace('\n', ' ')
        text = text.strip()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = " ".join([simplemma.lemmatize(x, self._lang_data) for x in text.split(' ') if len(x)])
        return text
