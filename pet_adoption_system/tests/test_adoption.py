def test_adopt_pet(test_client, get_token, create_user, create_admin,admin_credentials):
    # create admin:
    create_admin(admin_credentials["username"], "admin@example.com", admin_credentials["password"])

    # create user:
    create_user("adopter", "adopter@example.com", "pass123")
    user_token = get_token("adopter", "pass123")
    admin_token = get_token(admin_credentials["username"], admin_credentials["password"])

    pet = test_client.post("/admin/add_pet", json={
        "name": "Bruno",
        "breed": "Dog",
        "age": 2
    }, headers={"Authorization": f"Bearer {admin_token}"}).json()
    # print("Pet creation response:", pet)
    response = test_client.post(f"/pets/{pet['id']}/adopt", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Pet adopted successfully"

def test_return_pet(test_client, get_token, create_user,create_admin, admin_credentials):
    # create_admin(admin_credentials["username"], "admin@example.com", admin_credentials["password"])

    create_user("adopter2", "adopter2@example.com", "pass456")
    user_token = get_token("adopter2", "pass456")
    admin_token = get_token(admin_credentials["username"], admin_credentials["password"])

    pet = test_client.post("/admin/add_pet", json={
        "name": "Coco",
        "breed": "Parrot",
        "age": 1
    }, headers={"Authorization": f"Bearer {admin_token}"}).json()

    # print("Pet creation response:", pet)
    test_client.post(f"/pets/{pet['id']}/adopt", headers={"Authorization": f"Bearer {user_token}"})
    response = test_client.post(f"/pets/{pet['id']}/return", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Pet returned successfully"
