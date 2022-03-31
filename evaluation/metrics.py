from abc import ABCMeta, abstractmethod
from difflib import SequenceMatcher


class Metric(metaclass=ABCMeta):

    """Base class for metrics"""

    @property
    @abstractmethod
    def name(self) -> str:
        """put metric name here"""

    @abstractmethod
    def get_value(self, expected: str, predicted: str) -> float:
        """Implements metric evaluation logic"""


class JaccardSimilarity(Metric):

    @property
    def name(self) -> str:
        return "jaccard_similarity"

    def get_value(self, expected: str, predicted: str) -> float:

        """Jaccard similarity score.
        More: https://en.wikipedia.org/wiki/Jaccard_index

        Args:
            expected (list): reference list with str tokens
            predicted (list): target list with str tokens

        Returns:
            float: Jaccard score value
        """

        a = set(expected.split(" "))
        b = set(predicted.split(" "))
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))


class BuiltInMatcher(Metric):
    # TODO: This is just a placeholder, needs to be replaced with some serious metric

    @property
    def name(self) -> str:
        return "built_in_matcher"

    def get_value(self, expected: str, predicted: str) -> float:
        return SequenceMatcher(None, expected, predicted).ratio()