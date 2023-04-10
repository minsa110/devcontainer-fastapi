import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_list_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {}


def test_list_todo_not_found(client):
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_add_todo(client):
    response = client.post("/todos", params={"todo": "Buy groceries"})
    assert response.status_code == 200
    assert response.json() == {"todo_id": 1, "todo": "Buy groceries"}


def test_list_todo(client):
    client.post("/todos", params={"todo": "Buy groceries"})
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"todo_id": 1, "todo": "Buy groceries"}


def test_delete_todo(client):
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"result": "Todo deleted"}


def test_delete_todo_not_found(client):
    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}