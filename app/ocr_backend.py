from abc import ABCMeta, abstractmethod
from PIL import Image
from pytesseract import pytesseract
from easyocr import Reader
from typing import List
import numpy as np
import cv2

from app.language import AvailableLanguages, Script, Language
from app.exceptions import InvalidLanguageError

# TODO: expose OCR backend parameters


class OCRBackend(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self) -> str:
        """Backend name"""

    @abstractmethod
    def preprocess_image(self, image: Image) -> Image:
        """Backend dependent image preprocessing"""

    def _get_text(self, image: Image, language: List[Language]) -> str:
        """OCR library logic goes here"""

    def get_text(self, image: Image, languages: List[Language]) -> str:
        image = self.preprocess_image(image)
        return self._get_text(image, languages)


class TesseractBackend(OCRBackend):

    name = "tesseract"

    def preprocess_image(self, image: Image):
        image = np.array(image)
        # rescale should improve OCR quality
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        image = cv2.bilateralFilter(image, 7, 55, 60)
        _, image = cv2.threshold(src=image, thresh=180, maxval=255, type=cv2.THRESH_BINARY)
        image = Image.fromarray(image)
        return image

    def _get_text(self, image: Image, languages: List[Language]) -> str:
        return pytesseract.image_to_string(image=image, lang="+".join([l.abbr_3 for l in languages]))


class EasyOCRBackend(OCRBackend):

    def __init__(self, use_gpu: bool = False):
        self._cyrillic_reader: Reader = Reader([l.abbr_2 for l in AvailableLanguages().langs_cyrillic], gpu=use_gpu)
        self._latin_reader: Reader = Reader([l.abbr_2 for l in AvailableLanguages().langs_latin], gpu=use_gpu)

    name = "easy_ocr"

    def preprocess_image(self, image: Image):
        return image

    def _get_text(self, image: Image, languages: List[Language]) -> str:
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
