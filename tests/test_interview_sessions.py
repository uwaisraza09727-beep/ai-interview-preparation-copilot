from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_active_session():

    response = client.get(
        "/interview/session/active",
    )

    assert response.status_code in (
        200,
        400,
        401,
    )


def test_get_current_question():

    response = client.get(
        "/interview/session/current-question",
    )

    assert response.status_code in (
        200,
        400,
        401,
    )


def test_get_session_dashboard():

    response = client.get(
        "/interview/session/dashboard",
    )

    assert response.status_code in (
        200,
        400,
        401,
    )


def test_get_session_summary():

    response = client.get(
        "/interview/session/summary",
    )

    assert response.status_code in (
        200,
        400,
        401,
    )


def test_get_recent_sessions():

    response = client.get(
        "/interview/session/recent",
    )

    assert response.status_code in (
        200,
        401,
    )