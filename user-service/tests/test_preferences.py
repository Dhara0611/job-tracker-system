
def get_access_token(client):

    response = client.post("/api/v1/auth/login", json={
        "email":"user4@test.com",
        "password": "user4@123"
    })

    data = response.get_json()
    return data["access_token"]


def test_get_preferences_without_token(client):

    response = client.get("/api/v1/preferences/")
    assert response.status_code == 401


def test_save_preferences(client):

    token = get_access_token(client)
    response = client.post("api/v1/preferences/", 
        headers = {
            "Authorization": f"Bearer {token}"
        },
        json={
            "role": "Cloud Engineer",
            "experience": "Mid-Level",
            "location": "Santa Clara",
            "salary_min": 120000,
            "salary_max": 160000
        }
    )

    print(response.status_code)
    print(response.get_json())

    assert response.status_code == 200

def test_get_user_preferences(client):

    token = get_access_token(client)
    response = client.get("api/v1/preferences/", 
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )

    print(response.status_code)
    print(response.get_json())

    assert response.status_code == 200


def test_get_preferences_not_found(client):
    token = get_access_token(client)

    response = client.get("/api/v1/preferences/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 404





