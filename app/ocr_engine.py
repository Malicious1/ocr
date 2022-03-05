import pytesseract
from typing import List


class OCREngine:

    @staticmethod
    def get_text(image: bytes, language: str) -> str:
        return pytesseract.image_to_string(image, lang=language)

    @staticmethod
    def get_languages() -> List[str]:
        return pytesseract.get_languages()
