"""

Funkcja / Klasa: 
TaskScheduler 

Metody:
- add_task(name: str, priority: int) -> None
- pop_task() -> Optional[str]  # zwraca nazwę zadania o najwyższym priorytecie lub None, jeśli pusto

Wymagania:
1. Zadania o mniejszej wartości `priority` mają WYŻSZY priorytet (priority=0 > priority=10).
2. Kolejność zadań o tym samym priorytecie powinna być zgodna z kolejnością dodania (FIFO).
3. Zaimplementuj w oparciu o `heapq` (bez gotowych kolejek typu PriorityQueue).
4. Jeśli `pop_task()` wywołane na pustej kolejce → zwraca `None`.
5. Dodaj prosty test działania (np. dodaj 4 zadania i wypisz w kolejności wykonywania).

Przykład:
scheduler = TaskScheduler()
scheduler.add_task("fix bug", 2)
scheduler.add_task("write tests", 1)
scheduler.add_task("refactor", 1)
scheduler.pop_task()  # "write tests"
scheduler.pop_task()  # "refactor"
scheduler.pop_task()  # "fix bug"
"""
from __future__ import annotations
from heapq import heappush, heappop
from itertools import count
from typing import Optional


class TaskScheduler:
    """
    Min-heap scheduler: niższa wartość priority => wyższy priorytet.
    Dla równych priorytetów zachowuje kolejność dodania (FIFO).
    """
    def __init__(self):
        self._heap = []
        self._sec = count()

    def add_task(self, name: str, prio: int):
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        heappush(self._heap, (prio, next(self._sec), name))

    def pop_task(self) -> Optional[str]:
        if not self._heap:
            return None
        prio, index, name =  heappop(self._heap)
        return name
    
    def clear(self):
        self._heap.clear()
    
    def is_empty(self) -> bool:
        return not self._heap
    
    def peek(self) -> Optional[str]:
        return self._heap[0][2] if self._heap else None
    
    def __len__(self) -> int:
        return len(self._heap)
