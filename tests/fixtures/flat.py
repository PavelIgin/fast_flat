import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from flat.schemas import FlatCreate
from flat.service import flat_services
from users.models import User

__all__ = ("create_flat",)


@pytest.fixture(scope="session")
def create_flat(
    apply_migrations: None, created_user: User, db_connection: AsyncSession
):
    item = FlatCreate(
        **{
            "cost": 0,
            "photos": ["string"],
            "user": {
                "email": "user@example.com",
                "telegram_contact": "string",
            },
            "quadrature": 0,
            "floor": 0,
            "address": "string",
            "is_active": True,
        }
    )
    flat_services.post_flat_service(item, created_user, db_connection)
