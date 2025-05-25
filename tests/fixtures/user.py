import pytest

__all__ = ("created_user", "auth_user")


@pytest.fixture()
async def created_user(apply_migrations: None, client):
    """Main fixture of user."""
    data = {"email": "useaqqaar@example.com", "password": "stqring"}
    response = client.post(url="/auth/register/", json=data)
    assert response.status_code == 201
    return data


@pytest.fixture()
async def auth_user(created_user, client):
    """Main fixture of user."""
    response = client.post(
        url="/auth/jwt/login",
        data={
            "username": created_user["email"],
            "password": created_user["password"],
        },
    )
    return response.json()["access_token"]
