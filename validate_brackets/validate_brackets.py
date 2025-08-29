"""
Zadanie 1 — Walidacja nawiasów

Funkcja: validate_brackets(s: str) -> bool

Wymagania

Napisz funkcję, która sprawdza, czy w łańcuchu s wszystkie nawiasy są poprawnie zbalansowane i domknięte we właściwej kolejności.

Obsługiwane typy nawiasów: (), [], {}.

Inne znaki w s ignoruj — liczą się tylko nawiasy.

Zwróć True jeśli łańcuch jest poprawny, w przeciwnym razie False.

Przykłady (oczekiwane wyniki)

validate_brackets("()[]{}") == True

validate_brackets("([{}])") == True

validate_brackets("(]") == False

validate_brackets("([)]") == False

validate_brackets("abc(def)[ghi]{j}") == True

validate_brackets("(((") == False

validate_brackets("") == True

validate_brackets("]") == False

validate_brackets("{[}") == False

Edge cases do rozważenia

Pusty string.

Sekwencje z samymi „otwarciami” lub samymi „zamknięciami”.

Mieszane typy nawiasów z poprawną i niepoprawną kolejnością.

Kryteria akceptacji

Funkcja przechodzi powyższe przykłady.

Złożoność czasowa liniowa względem długości s.

Kod jest czytelny, z krótkim docstringiem i testami (np. pytest.mark.parametrize).

Czas pracy: 15 minut samodzielnie.
Gdy skończysz, wklej kod i testy — zrobię konkretne review.
"""
from collections import deque

def validate_brackets(s: str) -> bool:
    if not s:
        return True
    
    brackets = {'(': ')', "[": "]", "{": "}"}
    stack = deque()
    for c in s:
        if c in brackets:
            stack.append(brackets.get(c))
        elif c in brackets.values():
            if not stack or c != stack.pop():
                return False
        else:
            continue

    return not stack
