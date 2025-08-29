"""
Zadanie 2.1 — Kolejka priorytetowa z aktualizacją i anulowaniem zadań
Cel

Zaimplementuj strukturę (np. klasę PriorityScheduler), która obsługuje dynamiczne zarządzanie zadaniami wg priorytetu.

Niższa liczba = wyższy priorytet.

Stabilność: przy tym samym priorytecie zachowujemy kolejność dodania.

Operacje mają być amortyzacyjnie O(log n) (poza odczytami typu len, które mogą być O(1)).

Zasady

add: dodaje zadanie. Jeśli zadanie o tej nazwie już istnieje, potraktuj to jak reprioritize (zaktualizuj priorytet).

reprioritize: zmienia priorytet istniejącego zadania. Po zmianie zadanie zachowuje się tak, jakby zostało wstawione teraz (czyli przy remisie ustępuje wcześniejszym w tym samym priorytecie).

cancel: usuwa zadanie, jeśli istnieje; jeśli nie istnieje — operacja jest no-op (cicha).

run_next: zwraca nazwę zadania o najwyższym priorytecie i usuwa je z kolejki. Gdy pusto → None.

Nazwy zadań są unikatowe (jedno aktywne zadanie o danej nazwie).

Kryteria akceptacji

Poprawna stabilność przy remisach.

reprioritize działa jak „ponowne wstawienie” (zmienia pozycję w stabilnym porządku).

cancel działa cicho na nieistniejącym zadaniu.

run_next zwraca None przy pustej kolejce.

Złożoność operacji oparta o kolejkę priorytetową (np. heapq).

Edge-case’y do uwzględnienia

Wielokrotne reprioritize tego samego zadania przed uruchomieniem.

cancel tuż po reprioritize.

Dużo zadań o tym samym priorytecie (sprawdź stabilność).

add tego samego name traktowane jak aktualizacja (bez dublowania).

⏱ Czas pracy: spróbuj zamknąć pierwszą wersję w ~20 min.
Nie daję podpowiedzi — jak utkniesz, poproś o hint techniczny (np. „jak ogarnąć reprioritize z heapem bez kosztownego wyszukiwania?”).
"""
import heapq
from typing import Dict, Tuple, Optional, List

class PriorityScheduler:
    def __init__(self) -> None:
        # name -> (priority, seq)
        self._items: Dict[str, Tuple[int, int]] = {}
        self._seq: int = 0  # rosnący licznik "momentu wstawienia"

    def add(self, priority: int, name: str) -> None:
        # add tej samej nazwy traktujemy jak update (reprioritize+nowe wstawienie)
        self._items[name] = (priority, self._bump_seq())

    def reprioritize(self, name: str, new_priority: int) -> None:
        if name in self._items:
            self._items[name] = (new_priority, self._bump_seq())

    def cancel(self, name: str) -> None:
        self._items.pop(name, None)  # cicho jeśli nie istnieje

    def run_next(self) -> Optional[str]:
        if not self._items:
            return None
        # zbuduj kopiec: (priority, seq, name)
        heap: List[Tuple[int, int, str]] = [
            (prio, seq, name) for name, (prio, seq) in self._items.items()
        ]
        heapq.heapify(heap)
        prio, seq, name = heapq.heappop(heap)
        # usuń wybrane zadanie z aktywnych
        del self._items[name]
        return name

    def __len__(self) -> int:
        return len(self._items)

    def _bump_seq(self) -> int:
        self._seq += 1
        return self._seq
    