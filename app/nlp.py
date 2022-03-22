# NLP module of OCR app
import string
import simplemma
from typing import List


def remove_non_alphanum(text : str) -> str:
    """remove non alphanumeric characters from a string"""
    return text.translate(str.maketrans('', '', string.punctuation))


def simple_tokenizer(text : str, languages: List[str] = None) -> list:
    """Simple tokenizer

    Args:
        text (str): text to tokenize
        languages (list, optional): language list. Defaults to ['pl', 'en', 'ru', 'uk'].

    Returns:
        list: list of str tokens
    """
    if languages is None:
        languages = ['pl', 'en', 'ru', 'uk']
    langdata = simplemma.load_data(*languages)
    text = text.replace('\n', ' ')
    text = text.strip()
    text = text.lower()
    text = remove_non_alphanum(text)
    tokens = [simplemma.lemmatize(x, langdata) for x in text.split(' ') if len(x)]
    return tokens
