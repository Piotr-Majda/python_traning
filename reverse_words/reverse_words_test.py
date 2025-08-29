import pytest
from reverse_words import reverse_words


REVERSE_WORDS_CASE = [
    ('Hello World', 'olleH dlroW'),
    (' ab cd ', ' ba dc '),
    ('ABC', "CBA"),
]


@pytest.mark.parametrize('sentence,rev_words_sentence', REVERSE_WORDS_CASE)
def test_valid_if_has_reverse_words_character_in_sentence_ut(sentence, rev_words_sentence):
    r_s = reverse_words(sentence)
    assert r_s == rev_words_sentence
