# from tests.conftest import create_admin

# import pytest

def test_add_pet(test_client, get_token, admin_credentials,create_admin):
    create_admin(admin_credentials["username"], "admin@example.com", admin_credentials["password"])
    token = get_token(admin_credentials["username"], admin_credentials["password"])
    response = test_client.post("/admin/add_pet", json={
        "name": "Max",
        "breed": "Dog",
        "age": 4
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Max"

def test_add_pet_unauthorized(test_client):
    response = test_client.post("/admin/add_pet", json={
        "name": "Lucy",
        "breed": "Cat",
        "age": 3
    })
    assert response.status_code in [401, 403]

def test_get_all_pets(test_client):
    response = test_client.get("/pets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)