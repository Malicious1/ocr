from abc import ABCMeta, abstractmethod
from PIL import Image
from pytesseract import pytesseract
from easyocr import Reader
from typing import List
import numpy as np

from app.language import AvailableLanguages, Script, Language
from app.exceptions import InvalidLanguageError

# TODO: expose OCR backend parameters


class OCRBackend(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self) -> str:
        """Backend name"""

    @abstractmethod
    def get_text(self, image: Image, languages: List[Language]) -> str:
        """3rd party OCR libs go here"""


class TesseractBackend(OCRBackend):

    @property
    def name(self) -> str:
        return "tesseract"

    def get_text(self, image: Image, languages: List[Language]) -> str:
        return pytesseract.image_to_string(image=image, lang="+".join([l.abbr_3 for l in languages]))


class EasyOCRBackend(OCRBackend):

    def __init__(self, use_gpu: bool = False):
        self._cyrillic_reader: Reader = Reader([l.abbr_2 for l in AvailableLanguages().langs_cyrillic], gpu=use_gpu)
        self._latin_reader: Reader = Reader([l.abbr_2 for l in AvailableLanguages().langs_latin], gpu=use_gpu)

    @property
    def name(self) -> str:
        return "easy_ocr"

    def get_text(self, image: Image, languages: List[Language]) -> str:
        image = np.array(image)
        if all([l.script == Script.cyrillic for l in languages]):
            return " ".join(self._cyrillic_reader.readtext(image, detail=0))
        elif all([l.script == Script.latin for l in languages]):
            return " ".join(self._latin_reader.readtext(
                image,
                detail=0,
                decoder="beamsearch",
                beamWidth=10,
                batch_size=8,
                contrast_ths=0.4,
                adjust_contrast=0.7,
                width_ths=1))
        else:
            raise InvalidLanguageError("Not possible to mix both cyrillic and latin scripts with EasyOCR")

