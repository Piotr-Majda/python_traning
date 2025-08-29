'''
Zadanie #3 — Top-K słów (15 min kod + 5 min testy)

Funkcja: top_k_words(text: str, k: int) -> list[tuple[str, int]]

Wymagania:

Traktuj wielkość liter tak samo (normalizacja do lowercase).

Usuń podstawową interpunkcję: .,!?;: (reszta może zostać).

Licz słowa rozdzielone whitespace’em.

Zwróć k najczęstszych słów jako listę par (word, count).

Remisy: wygrywa słowo, które pierwsze pojawiło się w tekście (stabilny porządek po pierwszym wystąpieniu).

Bez bibliotek zewnętrznych (standard library OK).

Złożoność: celuj w O(n) czasu i O(u) pamięci (u = liczba unikalnych słów).

Przykład:

text = "Dog, dog! cat; Dog... bird cat"
top_k_words(text, 2) == [("dog", 3), ("cat", 2)]

Podpowiedzi (bez kodu)

Najpierw normalizacja (lower + prosty „strip” interpunkcji z końców/początków tokenów).

Potrzebujesz zarówno liczników, jak i indeksu pierwszego wystąpienia (dla tie-breakera).

Finalnie wybierasz top-k: albo sort po (-count, first_index), albo struktura top-k; przy małym k możesz rozważyć prosty sort (czytelność > mikro-optymalizacja).

Testy (pytest) — gotowe case’y z opisami (IDs)

Możesz skopiować same dane do swoich testów; nazwy case’ów w jednym miejscu via pytest.param:

import pytest

TOPK_CASES = [
    pytest.param("Dog, dog! cat; Dog... bird cat", 2, [("dog", 3), ("cat", 2)], id="basic_mixed_punct"),
    pytest.param("One one ONE; two, Two three", 2, [("one", 3), ("two", 2)], id="case_insensitive"),
    pytest.param("alpha beta gamma", 5, [("alpha",1),("beta",1),("gamma",1)], id="k_greater_than_unique"),
    pytest.param("", 3, [], id="empty_text"),
    pytest.param("tie tie win win x", 1, [("tie", 2)], id="tie_breaker_first_seen"),
]


Dodatkowo sprawdź:

duże wejście (np. 50k znaków) — czy działa w rozsądnym czasie,

k = 0 → wynik [],

słowa z polskimi znakami (powinno przejść).

Kryteria akceptacji

Przechodzi wszystkie powyższe testy.

Jedno źródło prawdy dla kolejności przy remisach (indeks pierwszego pojawienia).

Czytelny kod + krótki docstring + typy.

Brak zbędnych kopii danych.

Plan wykonania (20 min)

2–3 min: szkic podejścia na kartce.

10–12 min: implementacja.

5 min: testy + szybki refactor nazw/komentarzy.

Jak skończysz, wrzuć kod i logikę — zrobię review jak w PR (krótko i konkretnie). 🚀
'''
from collections import Counter

def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    # cleaning/normalization data
    text = text.lower()
    # text = text.strip('.,!?;:') # my previews though
    text = ''.join(e for e in text if e not in'.,!?;:') # my second though but after 15 min 
    # extract words by white space separators
    words = text.split()
    counter = Counter(words)
    return counter.most_common(k)
