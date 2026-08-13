from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_protected_route_without_token():

    response = client.get(
        "/users/me",
    )

    assert response.status_code == 401


def test_interview_answers_without_token():

    response = client.get(
        "/interview/answers/my",
    )

    assert response.status_code == 401


def test_interview_performance_without_token():

    response = client.get(
        "/interview/answers/performance",
    )

    assert response.status_code == 401


def test_interview_session_without_token():

    response = client.get(
        "/interview/session/active",
    )

    assert response.status_code == 401
    
def test_delete_interview_answer_without_token(
    client,
):

    response = client.delete(
        "/interview/answers/"
        "00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 401    
    
def test_get_my_answers_without_token(
    client,
):

    response = client.get(
        "/interview/answers/my"
    )

    assert response.status_code == 401    