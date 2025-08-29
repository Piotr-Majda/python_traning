"""
Zadanie #6 — Merge K Sorted Lists (użyj heapq)

Funkcja: merge_k_sorted(lists: list[list[int]]) -> list[int]
    # alternatywnie możesz zwrócić iterator: -> Iterator[int], ale standardowo zwróć listę

Wymagania:
1) Wejście to lista k posortowanych, rosnących list liczb całkowitych.
2) Zwróć jedną posortowaną listę zawierającą wszystkie elementy (z duplikatami).
3) Złożoność czasowa docelowo O(N log k), gdzie N = suma długości wszystkich list.
4) Pamięć dodatkowa: O(k) dla kopca.
5) Obsłuż przypadki brzegowe:
   - k == 0 (pusta lista wejściowa) → zwróć []
   - niektóre listy puste (np. [[], [1,2], []]) → działaj poprawnie
6) Użyj modułu `heapq` (bez gotowych struktur typu PriorityQueue).
7) Stabilność względem źródła nie jest wymagana, ale kolejność wartości ma być nierozerwalnie rosnąca.

Przykład:
Input:  [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]

Podpowiedź (jeśli utkniesz — możesz zignorować):
- Wrzucaj do kopca krotki: (wartość, indeks_listy, indeks_wiersza) i dopychaj następny element z tej listy po każdym `heappop`.
"""
from heapq import merge, heappop, heappush
from typing import List


def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    if not lists:
        return []
    
    return list(merge(*lists))


def merge_k_sorted_manual_not_optimal(lists: list[list[int]]) -> list[int]:
    if not lists:
        return []
    
    max_heap_size = 0
    heap = []
    manual_list = []
    for index, elements in enumerate(lists):
        for i, ele in enumerate(elements):
            heappush(heap, (ele, index, i))
    
    max_heap_size = len(heap)
    
    while heap:
        ele, _, _ = heappop(heap)
        manual_list.append(ele)

    print(f"Max heap size {max_heap_size}")
    return manual_list

"""
Co jest teraz nieoptymalne

Wrzucasz do kopca wszystkie elementy (pętla po całych listach).

To daje O(N log N) czasu i O(N) pamięci — praktycznie sortowanie wszystkiego kopcem.

heapify(lists) nie ma sensu — to robi kopiec z listy list (z porównaniem po pierwszych elementach), a i tak go nie używasz.

Jak to naprawić (wzorzec “k pointers + heap”)

Do kopca wrzuć tylko pierwszy element z każdej niepustej listy: (wartość, idx_listy, idx_w_liscie).

Za każdym heappop dopchnij następny element z tej samej listy.

Poprawiona wersja (O(N log k), O(k) pamięci)

Dlaczego Twoja wersja jest O(N log N) i O(N) pamięci

W Twojej wersji:

wrzucasz każdy element wszystkich list do kopca,

kopiec ma więc rozmiar ~N (suma wszystkich elementów),

każda operacja heappush/heappop kosztuje O(log N),

wykonujesz ~N operacji ⇒ N · log N,

dodatkowa pamięć na kopiec to O(N).

To de facto „posortuj wszystko kopcem” (heap sort), tylko że startujesz już z posortowanych list, czego nie wykorzystujesz.

Cel: O(N log k) i O(k) pamięci

Zauważ, że masz k list już posortowanych. W każdym momencie wystarczy znać tylko najmniejsze „czołówki” z każdej listy — czyli k kandydatów na najbliższy element wyniku.

Wzorzec „k pointers + heap” (intuicja)

Trzymasz po jednym wskaźniku (pointerze) na aktualną pozycję w każdej z k list (stąd „k pointers”).

Do kopca wkładasz tylko pierwszy dostępny element z każdej niepustej listy ⇒ kopiec ma ≤ k elementów.

Zdejmujesz minimum (heappop) → dostajesz następny element wyniku.

I tylko wtedy dopychasz kolejny element z tej samej listy, z której pochodziło zdjęte minimum.

Dzięki temu kopiec cały czas ma wielkość k, niezależnie od N.

Złożoność

Wykonasz N popów i do N pushy (każdy element wchodzi do kopca dokładnie raz, tuż przed użyciem).

Każda operacja kosztuje O(log k), bo kopiec ma rozmiar ≤ k.
→ O(N log k) czasu i O(k) pamięci.

Czy „wrzucić całą listę naraz”?

Nie. Wrzucasz po jednym elemencie na listę.
Jeśli wrzucisz całą listę, to wracasz do O(N log N).
Klucz: leniwe doładowywanie — dokładnie jeden nowy element z tej listy, z której właśnie pobrałeś minimum.

Krótki przykład krok po kroku

Listy:
A = [1, 4, 10]
B = [2, 3, 11]
C = [0, 5, 6]

Start: kopiec = {(1,A0), (2,B0), (0,C0)} ← 3 elementy (k=3)
Pop → (0,C0), wynik=[0], push następny z C → (5,C1)
Kopiec = {(1,A0), (2,B0), (5,C1)}
Pop → (1,A0), wynik=[0,1], push (4,A1)
Kopiec = {(2,B0), (5,C1), (4,A1)}
… itd. Zawsze ≤ k w kopcu.

"""

def merge_k_sorted_manual(lists: List[List[int]]) -> List[int]:
    if not lists:
        return []
    max_heap_size = 0
    heap: list[tuple[int, int, int]] = []  # (value, list_idx, elem_idx)
    out: List[int] = []

    # 1) inicjalizacja kopca pierwszymi elementami
    for li, lst in enumerate(lists):
        if lst:  # tylko niepuste
            heappush(heap, (lst[0], li, 0))
    max_heap_size = len(heap)
    # 2) zdejmuj minimum i dopychaj kolejny z tej samej listy
    while heap:
        val, li, i = heappop(heap)
        out.append(val)
        nxt = i + 1
        if nxt < len(lists[li]):
            heappush(heap, (lists[li][nxt], li, nxt))
        max_heap_size = len(heap) if len(heap) > max_heap_size else max_heap_size
    print(f"Max heap size {max_heap_size}")
    return out

