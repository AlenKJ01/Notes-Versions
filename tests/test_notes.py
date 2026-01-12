def auth_headers(client):
    client.post(
        "/auth/register",
        json={"email": "note@test.com", "password": "secret"}
    )
    r = client.post(
        "/auth/login",
        data={"username": "note@test.com", "password": "secret"}
    )
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_get_note(client):
    headers = auth_headers(client)

    r = client.post(
        "/notes/",
        json={"title": "Test", "content": "Hello"},
        headers=headers
    )
    assert r.status_code == 200
    note = r.json()
    assert note["title"] == "Test"

    r = client.get("/notes/", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_update_creates_version(client):
    headers = auth_headers(client)

    r = client.post(
        "/notes/",
        json={"title": "Versioned", "content": "v1"},
        headers=headers
    )
    note_id = r.json()["id"]

    r = client.put(
        f"/notes/{note_id}",
        json={"content": "v2"},
        headers=headers
    )
    assert r.status_code == 200

    r = client.get(
        f"/notes/{note_id}/versions",
        headers=headers
    )
    versions = r.json()
    assert len(versions) == 2
    assert versions[1]["version_number"] == 2
