
def test_register_new_user(client):
    response = client.post("/api/v1/auth/register", json = {
        "email" : "user4@test.com",
        "password" : "user4@123"
    })

    print(response.status_code)
    print(response.get_json())

    assert response.status_code == 201

def test_login_user(client):
    response = client.post("/api/v1/auth/login", json={
        "email":"user4@test.com",
        "password": "user4@123"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_login_invalid_password(client):

    response = client.post("/api/v1/auth/login", json = {
        "email":"user2@test.com",
        "password":"user3@123"
    })

    assert response.status_code == 401


def test_register_existing_user(client):
    response = client.post("/api/v1/auth/register", json = {
        "email" : "user2@test.com",
        "password" : "user1@123"
    })

    assert response.status_code == 400






