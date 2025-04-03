from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup():
    response = client.post("/auth/signup", json={
        "username": "admin5",
        "email": "admin5@example.com",
        "password": "admin5"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "admin5@example.com"