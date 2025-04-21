def test_get_current_user(test_client, get_token, create_user):
    create_user("profileuser", "profile@example.com", "userpass")
    token = get_token("profileuser", "userpass")

    response = test_client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "profileuser"

def test_update_user_details(test_client, get_token, create_user):
    create_user("updateuser", "update@example.com", "userpass")
    token = get_token("updateuser", "userpass")

    update_data = {
        "username": "updateduser",
        "email": "updated@example.com",
        "password": "newpass"
    }

    response = test_client.put("/auth/me", json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"
    assert response.json()["email"] == "updated@example.com"
