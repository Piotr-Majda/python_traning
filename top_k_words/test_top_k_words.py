import pytest
from top_k_words import top_k_words

TOPK_CASES = [
    pytest.param("Dog, dog! cat; Dog... bird cat", 2, [("dog", 3), ("cat", 2)], id="basic_mixed_punct"),
    pytest.param("One one ONE; two, Two three", 2, [("one", 3), ("two", 2)], id="case_insensitive"),
    pytest.param("alpha beta gamma", 5, [("alpha",1),("beta",1),("gamma",1)], id="k_greater_than_unique"),
    pytest.param("", 3, [], id="empty_text"),
    pytest.param("tie tie win win x", 1, [("tie", 2)], id="tie_breaker_first_seen"),
]


@pytest.mark.parametrize('text,k,excepted_output', TOPK_CASES)
def test_top_k_words_ut(text, k, excepted_output):
    top_words = top_k_words(text, k)
    assert top_words == excepted_output
