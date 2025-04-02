import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def admin_token():
    response = client.post("/auth/login", json={"username": "admin", "password": "adminpass"})
    return response.json()["access_token"]

@pytest.fixture
def test_pet(admin_token):
    pet_data = {"name": "Buddy", "species": "Dog", "age": 3}
    response = client.post("/admin/pets", json=pet_data, headers={"Authorization": f"Bearer {admin_token}"})
    return response.json()

# Test Adding a Pet (Admin Only)
def test_add_pet(admin_token):
    pet_data = {"name": "Charlie", "species": "Cat", "age": 2}
    response = client.post("/admin/pets", json=pet_data, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    assert response.json()["name"] == "Charlie"

# Test Adding a Pet Without Auth
def test_add_pet_unauthorized():
    pet_data = {"name": "Rocky", "species": "Dog", "age": 5}
    response = client.post("/admin/pets", json=pet_data)
    assert response.status_code == 403

# Test Updating a Pet
def test_update_pet(admin_token, test_pet):
    updated_data = {"name": "Buddy", "species": "Dog", "age": 4}
    pet_id = test_pet["id"]
    response = client.put(f"/admin/pets/{pet_id}", json=updated_data, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["age"] == 4
