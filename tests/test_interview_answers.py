from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_my_answers():

    response = client.get(
        "/interview/answers/my",
    )

    assert response.status_code in (
        200,
        401,
    )


def test_get_performance():

    response = client.get(
        "/interview/answers/performance",
    )

    assert response.status_code in (
        200,
        401,
    )


def test_get_invalid_answer_id():

    response = client.get(
        "/interview/answers/not-a-uuid",
    )

    assert response.status_code in (
        401,
        422,
    )
    
def test_evaluate_answer_question_not_found(
    client,
):

    response = client.post(
        "/interview/answers/evaluate",
        json={
            "interview_question_id": (
                "00000000-0000-0000-0000-000000000000"
            ),
            "answer": "Test answer",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Interview question not found"
    }  
    
def test_get_invalid_answer_id(
    client,
):

    response = client.get(
        "/interview/answers/not-a-valid-uuid"
    )

    assert response.status_code == 422      