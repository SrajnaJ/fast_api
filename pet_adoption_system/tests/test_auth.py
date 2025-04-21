def test_signup(create_user):
    response = create_user("testuser", "testuser@example.com", "testpass")
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_login(test_client, create_user):
    create_user("loginuser", "login@example.com", "loginpass")
    response = test_client.post("/auth/login", data={
        "username": "loginuser",
        "password": "loginpass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user(test_client):
    response = test_client.post("/auth/login", data={
        "username": "wrong",
        "password": "wrongpass"
    })
    assert response.status_code == 401