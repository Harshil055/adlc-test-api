import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# --- Existing tests ---

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_read_item():
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json()["item_id"] == 42


def test_read_item_with_query():
    response = client.get("/items/1?q=test")
    assert response.status_code == 200
    assert response.json()["q"] == "test"


def test_create_item():
    response = client.post("/items", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201
    assert response.json()["name"] == "Widget"
    assert response.json()["price"] == 9.99


# --- /password-reset/request ---

def test_password_reset_request_valid_email():
    response = client.post("/password-reset/request", json={"email": "user@example.com"})
    assert response.status_code == 200
    assert "reset" in response.json()["message"].lower()


def test_password_reset_request_invalid_email():
    response = client.post("/password-reset/request", json={"email": "notanemail"})
    assert response.status_code == 422


def test_password_reset_request_empty_email():
    response = client.post("/password-reset/request", json={"email": ""})
    assert response.status_code == 422


# --- /password-reset/confirm ---

def test_password_reset_confirm_valid():
    response = client.post("/password-reset/confirm", json={
        "token": "some-valid-token",
        "new_password": "securepassword123"
    })
    assert response.status_code == 200
    assert "success" in response.json()["message"].lower()


def test_password_reset_confirm_short_password():
    response = client.post("/password-reset/confirm", json={
        "token": "some-valid-token",
        "new_password": "short"
    })
    assert response.status_code == 422


def test_password_reset_confirm_empty_token():
    response = client.post("/password-reset/confirm", json={
        "token": "",
        "new_password": "securepassword123"
    })
    assert response.status_code == 422


def test_password_reset_confirm_missing_fields():
    response = client.post("/password-reset/confirm", json={})
    assert response.status_code == 422
