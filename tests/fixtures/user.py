import pytest

__all__ = ("user", "auth_user")

from fastapi_users import BaseUserManager, models
from fastapi_users.db import BaseUserDatabase
from fastapi_users.manager import UserManagerDependency
from fastapi_users.schemas import BaseUserCreate
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from base.base import User


@pytest.fixture(scope="session")
async def user(client, db_session):
    """Main fixture of user."""
    data = dict(email="useaqqaar@example.com", password="string")
    schema = BaseUserCreate(email="useaqqaar@example.com", password="string")
    user = await BaseUserManager(
        SQLAlchemyUserDatabase(session=db_session, user_table=User)
    ).create(user_create=schema)
    data["id"] = user.id
    return data


@pytest.fixture()
async def auth_user(user, client) -> dict:
    """Main fixture of user."""
    response = client.post(
        url="/auth/jwt/login",
        data={
            "username": user["email"],
            "password": user["password"],
        },
    )
    return response.json()["access_token"]
