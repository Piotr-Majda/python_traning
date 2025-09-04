"""
Endpoint POST /tasks – tworzy nowe zadanie (title: str, done: bool = False).

Endpoint GET /tasks – zwraca listę wszystkich zadań.

Endpoint PATCH /tasks/{task_id} – pozwala zmienić status done na True/False.

Endpoint DELETE /tasks/{task_id} – usuwa zadanie.
"""

import pytest
from fastapi.testclient import TestClient

from todo_list_api.api import app


@pytest.fixture(scope="function")
def client() -> TestClient:
    # Reset global state before each test
    from todo_list_api import api

    api.tasks.clear()
    api.ids.clear()
    return TestClient(app)


def test_create_new_task(client):
    r = client.post("/tasks", json={"title": "fix bug"})
    assert r.status_code == 201
    assert r.json() == {"title": "fix bug", "done": False, "id": 1}


def test_get_tasks(client):
    r = client.post("/tasks", json={"title": "fix bug"})

    assert r.status_code == 201
    assert r.json() == {"title": "fix bug", "done": False, "id": 1}

    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json()[0] == {"title": "fix bug", "done": False, "id": 1}


def test_patch_tasks(client):
    r = client.post("/tasks", json={"title": "fix bug"})

    assert r.status_code == 201
    assert r.json() == {"title": "fix bug", "done": False, "id": 1}

    r = client.patch("/tasks/1", json={"done": True})
    assert r.status_code == 200
    assert r.json() == {"title": "fix bug", "done": True, "id": 1}


def test_delete_tasks(client):
    r = client.post("/tasks", json={"title": "fix bug"})

    assert r.status_code == 201
    assert r.json() == {"title": "fix bug", "done": False, "id": 1}

    r = client.delete("/tasks/1")
    assert r.status_code == 204
