Napisz w FastAPI prostą usługę do zarządzania zadaniami (todo list).

Wymagania:

Endpoint POST /tasks – tworzy nowe zadanie (title: str, done: bool = False).

Endpoint GET /tasks – zwraca listę wszystkich zadań.

Endpoint PATCH /tasks/{task_id} – pozwala zmienić status done na True/False.

Endpoint DELETE /tasks/{task_id} – usuwa zadanie.

Ograniczenia:

Użyj tylko pamięci (list / dict) jako storage, bez bazy.

Zastosuj Pydantic modele.

Obsłuż sytuację, gdy task_id nie istnieje (np. 404).