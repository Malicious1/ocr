from evaluation.metrics import JaccardSimilarity

import pytest


@pytest.mark.parametrize(
    ("text_1", "text_2", "score"),
    (
        ("a a", "a", 1.0),
        ("a a", "a b", 0.5),
        ("a a", "", 0.0),
        ("1 0 1 2", "1 3 3", 0.25)
    ),
)
def test_jaccard_similarity(text_1, text_2, score):
    assert JaccardSimilarity().get_value(text_1, text_2) == score
