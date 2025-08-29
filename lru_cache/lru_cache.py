"""
Zadanie 4️⃣ — LRU Cache

Zaimplementuj klasę LRUCache, która działa jak pamięć podręczna o ograniczonym rozmiarze i usuwa najdawniej używany element (Least Recently Used), gdy przekroczony zostanie limit.

Wymagania:

Konstruktor przyjmuje capacity: int (maksymalna liczba elementów w cache).

Metody:

get(key: str) -> int | None — zwraca wartość z cache (lub None, jeśli klucza nie ma). Dostęp do elementu odświeża jego użycie.

put(key: str, value: int) -> None — dodaje lub aktualizuje element. Jeśli cache jest pełny, usuń najdawniej używany.

__len__(self) -> int — liczba elementów w cache.

Operacje powinny działać w czasie O(1) średnio.

📌 Twoim zadaniem jest wymyślenie, jakiej struktury danych użyć, żeby połączyć szybki dostęp do kluczy i jednocześnie wiedzieć, które były najdawniej używane.
"""
from collections import OrderedDict
from typing import Optional

class LruCache:
    """
    Least Recently Used (LRU) LRU picks the data that is least recently used 
    and removes it in order to make space for the new data. 
    The priority of the data in the cache changes according to the need of that data 
    if some data is fetched or updated recently then the priority of that data would be 
    changed and assigned to the highest priority , and the priority of the data decreases 
    if it remains unused operations after operations. 
    """
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.__capacity = capacity
        self.__cache: OrderedDict[str, int] = OrderedDict()

    @property
    def capacity(self) -> int:
        return self.__capacity

    def put(self, key: str, value: int) -> None:
        # jeśli klucz istnieje — przesuwamy go na koniec (najświeższy)
        if key in self.__cache:
            self.__cache.move_to_end(key)
        self.__cache[key] = value
        # po wstawieniu pilnujemy limitu
        if len(self.__cache) > self.__capacity:
            self.__cache.popitem(last=False)  # wyrzuć najstarszy

    def get(self, key: str) -> Optional[int]:
        if key not in self.__cache:
            return None
        self.__cache.move_to_end(key)  # odśwież użycie
        return self.__cache[key]

    def __len__(self) -> int:
        return len(self.__cache)
