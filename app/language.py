from typing import List
from dataclasses import dataclass
import inspect


@dataclass
class Language:
    tesseract_name: str
    simplelemma_name: str


class AvailableLanguages:

    """Add new languages below"""

    polish = Language("pol", "pl")
    english = Language("eng", "en")
    ukrainian = Language("ukr", "uk")
    russian = Language("rus", "ru")

    def __init__(self):
        self._languages = [e[1] for e in inspect.getmembers(self) if isinstance(e[1], Language)]

    @property
    def languages(self) -> List[Language]:
        return self._languages

    @property
    def langs4tesseract(self) -> List[str]:
        return [l.tesseract_name for l in self.languages]

    @property
    def langs4simplelemma(self) -> List[str]:
        return [l.simplelemma_name for l in self.languages]


