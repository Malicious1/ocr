from typing import List
from dataclasses import dataclass
import inspect
from enum import Enum


class Script(Enum):

    cyrillic = 1
    latin = 2


@dataclass
class Language:
    abbr_3: str
    abbr_2: str
    script: Script


class AvailableLanguages:

    """Add new languages below"""

    polish = Language("pol", "pl", Script.latin)
    english = Language("eng", "en", Script.latin)
    ukrainian = Language("ukr", "uk", Script.cyrillic)
    russian = Language("rus", "ru", Script.cyrillic)

    def __init__(self):
        self._languages = [e[1] for e in inspect.getmembers(self) if isinstance(e[1], Language)]

    @property
    def languages(self) -> List[Language]:
        return self._languages

    @property
    def langs_abbr_3(self) -> List[str]:
        return [l.abbr_3 for l in self.languages]

    @property
    def langs_abbr_2(self) -> List[str]:
        return [l.abbr_2 for l in self.languages]

    @property
    def langs_cyrillic(self) -> List[Language]:
        return [l for l in self.languages if l.script == Script.cyrillic]

    @property
    def langs_latin(self) -> List[Language]:
        return [l for l in self.languages if l.script == Script.latin]
    
    def get_langs(self, abbr_3_langs: List[str]) -> List[Language]:
        return [l for l in self.languages if l.abbr_3 in abbr_3_langs]


