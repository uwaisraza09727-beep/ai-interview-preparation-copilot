from fastapi.testclient import TestClient


def test_invalid_interview_answer_request(
    client: TestClient,
):

    response = client.post(
        "/interview/answers/evaluate",
        json={},
    )

    assert response.status_code == 422