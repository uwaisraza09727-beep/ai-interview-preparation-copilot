import uuid

import pytest

from fastapi.testclient import TestClient

from app.main import app

from app.core.dependencies.auth import (
    get_current_user,
)

from app.models.user import User


mock_user = User(
    id=uuid.uuid4(),
    full_name="Test User",
    email="test@example.com",
    role="user",
    is_active=True,
)


async def override_get_current_user():

    return mock_user


@pytest.fixture
def client():

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    with TestClient(app) as test_client:

        yield test_client

    app.dependency_overrides = {}