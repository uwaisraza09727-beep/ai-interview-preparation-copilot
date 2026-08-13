from fastapi.testclient import TestClient


def test_get_current_user(
    client: TestClient,
):

    response = client.get(
        "/users/me"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == (
        "test@example.com"
    )

    assert data["full_name"] == (
        "Test User"
    )

    assert data["role"] == (
        "user"
    )

    assert data["is_active"] is True