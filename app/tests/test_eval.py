import pytest
from app.eval import *

@pytest.mark.parametrize(
    ("list_1", "list_2", "score"),
    (
        (["a","a"], ["a"], 1.0),
        (["a","a"], ["a","b"], 0.5),
        (["a","a"],[], 0.0),
        ([1,0,1,2], [1, 3, 3], 0.25)
    ),
)
def test_jaccard_similarity(list_1, list_2, score):
    assert jaccard_similarity(list_1, list_2) == score
