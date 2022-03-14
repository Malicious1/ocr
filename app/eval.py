# Evaluation module of OCR app
from typing import Callable

from PIL import Image

from .nlp import simple_tokenizer

def jaccard_similarity(tokens1 : list, tokens2 : list) -> float:
    """Jaccard similarity score.
    More: https://en.wikipedia.org/wiki/Jaccard_index

    Args:
        tokens1 (list): reference list with str tokens
        tokens2 (list): target list with str tokens

    Returns:
        float: Jaccard score value
    """
    a = set(tokens1) 
    b = set(tokens2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def evaluate_ocr(ocr : Callable, evaluation_data : dict,
                 metric : Callable[list, list] = jaccard_similarity,
                 silent = True) -> dict:
    """Perform evaluation of OCR according to the specified metric.

    Args:
        ocr (OCREngine): ocr function
        evaluation_data (dict): dictionary with pairs (image path, text)
        metric (Callable) : function with metric score (needs to accept string tokens)
        silent (bool) flag that says whether output should be printed for individual scores

    Returns:
        dict : dictionary with scores for images
    """
    scores = {}
    for img_path, text in evaluation_data.items():
        with Image.open(img_path) as img:
            ocr_text = ocr(img)
        ocr_tokens = simple_tokenizer(ocr_text)
        ref_tokens = simple_tokenizer(text)
        sc_ = jaccard_similarity(ocr_tokens, ref_tokens)
        scores[img_path] = sc_
        if not silent:
            print('>>>', img_path)
            print('Ref text :: ', text)
            print('OCR text :: ', ocr_text)
            print('Score :: ', sc_)
            print('_' * 10)
    return scores

