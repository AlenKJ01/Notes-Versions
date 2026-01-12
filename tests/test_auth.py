def test_register_and_login(client):
    # register
    r = client.post(
        "/auth/register",
        json={"email": "user@test.com", "password": "secret123"}
    )
    assert r.status_code == 200

    # login
    r = client.post(
        "/auth/login",
        data={"username": "user@test.com", "password": "secret123"}
    )
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure(client):
    r = client.post(
        "/auth/login",
        data={"username": "ghost@test.com", "password": "nope"}
    )
    assert r.status_code == 401
