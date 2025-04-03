import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#Fixture for getting an authenticated user token
@pytest.fixture
def user_token():
    user_data = {"admin": "useradmin", "password": "useradmin"}
    client.post("/auth/signup", json=user_data)  # Create test user
    response = client.post("/auth/login", json=user_data)
    return response.json()["access_token"]

#Fixture for getting an admin token (to create pets)
@pytest.fixture
def admin_token():
    response = client.post("/auth/login", json={"username": "admin5", "password": "admin5"})
    return response.json()["access_token"]

#Fixture for adding a test pet (only admin can add)
@pytest.fixture
def test_pet(admin_token):
    pet_data = {"name": "Buddy", "species": "Dog", "age": 3}
    response = client.post("/admin/pets", json=pet_data, headers={"Authorization": f"Bearer {admin_token}"})
    return response.json()

# Test adopting a pet (valid case)
def test_adopt_pet(user_token, test_pet):
    pet_id = test_pet["id"]
    response = client.post(f"/pets/{pet_id}/adopt", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Pet adopted successfully"

#Test adopting a pet without authentication
def test_adopt_pet_unauthorized(test_pet):
    pet_id = test_pet["id"]
    response = client.post(f"/pets/{pet_id}/adopt")
    assert response.status_code == 401  # Unauthorized

#Test adopting a pet that does not exist
def test_adopt_nonexistent_pet(user_token):
    response = client.post("/pets/999/adopt", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 404  # Pet not found

# Test returning a pet (valid case)
def test_return_pet(user_token, test_pet):
    pet_id = test_pet["id"]
    client.post(f"/pets/{pet_id}/adopt", headers={"Authorization": f"Bearer {user_token}"})  # First adopt the pet
    response = client.post(f"/pets/{pet_id}/return", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Pet returned successfully"

#  Test returning a pet that wasn't adopted
def test_return_unadopted_pet(user_token, test_pet):
    pet_id = test_pet["id"]
    response = client.post(f"/pets/{pet_id}/return", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 400  # Bad request, pet wasn't adopted

#  Test returning a pet without authentication
def test_return_pet_unauthorized(test_pet):
    pet_id = test_pet["id"]
    response = client.post(f"/pets/{pet_id}/return")
    assert response.status_code == 401  # Unauthorized

#Test adoption history (valid case)
def test_adoption_history(user_token):
    response = client.get("/pets/history", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)  

#Test adoption history without authentication
def test_adoption_history_unauthorized():
    response = client.get("/pets/history")
    assert response.status_code == 401  # Unauthorized
