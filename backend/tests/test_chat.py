import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Chatbot API"}

def test_send_message_success():
    response = client.post(
        "/api/v1/chat/",
        json={"message": "Hello, chatbot!"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == "Echo: Hello, chatbot!"

def test_send_empty_message():
    response = client.post(
        "/api/v1/chat/",
        json={"message": "   "}
    )
    assert response.status_code == 422  # Validation error

def test_send_message_too_long():
    long_message = "a" * 1001
    response = client.post(
        "/api/v1/chat/",
        json={"message": long_message}
    )
    assert response.status_code == 422  # Validation error

def test_send_message_missing_field():
    response = client.post(
        "/api/v1/chat/",
        json={}
    )
    assert response.status_code == 422  # Validation error

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}