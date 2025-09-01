Zadanie #9 — LRU Document Cache API (FastAPI, bez baz danych)

Cel:
Zaimplementuj REST API do zarządzania per-user cache’em dokumentów z polityką LRU (Least Recently Used).
Cache jest w pamięci procesu. Brak persystencji.

Wymagania funkcjonalne:
1) Cache per użytkownik (klucz: user_id).
2) Każdy wpis: {doc_id: str, content: str, updated_at: ISO8601}.
3) Polityka LRU:
   - odczyt (GET doc) i zapis (POST/PUT) promują element na „najświeższy”,
   - przy przekroczeniu pojemności usuń najrzadziej używany.
4) Pojemność konfigurowalna per user (domyślnie 3).
5) Zmiana pojemności < aktualny rozmiar → natychmiastowe wyparcie LRU.
6) Brak zewn. bibliotek do LRU — zrób własną strukturę: słownik + dwukierunkowa lista (node: prev,next,doc_id).

Endpoints (JSON in/out):
- PUT /users/{user_id}/settings
  body: {"capacity": int >= 1}
  200: {"user_id","capacity","size"}
  400: walidacja

- POST /users/{user_id}/cache
  body: {"doc_id": str, "content": str}
  201: {"doc_id","content","updated_at"}
  200: jeśli doc istnieje → nadpisz content i promuj do MRU
  400: walidacja

- GET /users/{user_id}/cache/{doc_id}
  200: {"doc_id","content","updated_at"}
  404: brak
  *Promuje element (MRU).*

- PUT /users/{user_id}/cache/{doc_id}
  body: {"content": str}
  200: {"doc_id","content","updated_at"}
  404: brak (nie twórz implicit)

- DELETE /users/{user_id}/cache/{doc_id}
  204 bez body
  404: brak

- GET /users/{user_id}/cache
  query: order ∈ {"mru","lru"} (domyślnie "mru")
  200: {"items":[{"doc_id","updated_at"}], "size": int, "capacity": int}
  *Zwróć listę bez content (lista przeglądowa).*

Zasady API:
- Content-Type: application/json.
- Błędy → 4xx/5xx z {"detail": "..."}.
- Idempotencja:
  - PUT/DELETE są idempotentne,
  - POST z tym samym doc_id traktuj jako aktualizację (200).
- Walidacja: puste doc_id/content → 400.

Wymagania niefunkcjonalne:
- Język: Python 3.11+.
- Framework: FastAPI.
- LRU: własna implementacja (dict + doubly linked list), O(1) dla get/put/promote/evict.
- Kod rozdziel: warstwa LRU (klasa) + warstwa HTTP (FastAPI).
- Brak testów w tym zadaniu.

Przykładowa sekwencja akceptacyjna (informacyjnie):
1) PUT /users/u1/settings {"capacity":2} → 200 size=0
2) POST /users/u1/cache {"doc_id":"a","content":"A"} → 201
3) POST /users/u1/cache {"doc_id":"b","content":"B"} → 201
4) GET  /users/u1/cache → items w kolejności MRU: ["b","a"]
5) POST /users/u1/cache {"doc_id":"c","content":"C"} → 201 (wyparuj "a")
6) GET  /users/u1/cache/a → 404
7) GET  /users/u1/cache/b → 200 (promuj "b")
8) PUT  /users/u1/cache/c {"content":"C2"} → 200 (promuj "c")
9) GET  /users/u1/cache?order=lru → items: ["b","c"]

Dostarcz:
- lru.py — klasa LRUCache (put/get/delete/list/set_capacity) z O(1).
- api.py — FastAPI z endpointami jak wyżej.
