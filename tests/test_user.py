import pytest
from fastapi.testclient import TestClient


@pytest.mark.anyio
async def test_create_user(client: TestClient):
    response = client.post(
        url="/auth/register/",
        json={"email": "useaaar@example.com", "password": "string"},
    )
    assert response.status_code == 201


@pytest.mark.anyio
async def test_login_user(client: TestClient, created_user: dict):
    response = client.post(
        url="/auth/jwt/login",
        data={
            "username": created_user["email"],
            "password": created_user["password"],
        },
    )
    assert response.status_code == 200
