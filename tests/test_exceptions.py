from fastapi.testclient import TestClient


def test_answer_not_found(
    client: TestClient,
):

    answer_id = (
        "ad5224a7-c219-4a38-8b52-9195c82a9080"
    )

    response = client.get(
        f"/interview/answers/{answer_id}"
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Answer not found"
    }