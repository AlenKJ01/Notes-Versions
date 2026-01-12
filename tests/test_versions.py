def auth_headers(client, email):
    client.post(
        "/auth/register",
        json={"email": email, "password": "secret"}
    )
    r = client.post(
        "/auth/login",
        data={"username": email, "password": "secret"}
    )
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_restore_creates_new_version(client):
    headers = auth_headers(client, "restore@test.com")

    r = client.post(
        "/notes/",
        json={"title": "Restore", "content": "v1"},
        headers=headers
    )
    note_id = r.json()["id"]

    client.put(
        f"/notes/{note_id}",
        json={"content": "v2"},
        headers=headers
    )

    r = client.post(
        f"/notes/{note_id}/versions/1/restore",
        headers=headers
    )
    assert r.status_code == 200

    r = client.get(
        f"/notes/{note_id}/versions",
        headers=headers
    )
    versions = r.json()
    assert len(versions) == 3
    assert versions[-1]["version_number"] == 3
    assert versions[-1]["content_snapshot"] == "v1"


def test_cross_user_access_blocked(client):
    h1 = auth_headers(client, "a@test.com")
    h2 = auth_headers(client, "b@test.com")

    r = client.post(
        "/notes/",
        json={"title": "Private", "content": "secret"},
        headers=h1
    )
    note_id = r.json()["id"]

    r = client.get(
        f"/notes/{note_id}/versions",
        headers=h2
    )
    assert r.status_code == 404 or r.status_code == 403
