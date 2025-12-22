import pytest
from repositories import FlatRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from flat.models import Flat
from flat.schemas import FlatCreate
from users.models import User

__all__ = ("flat",)


@pytest.fixture()
async def flat(user: User, db_session: AsyncSession):
    data = dict(
        cost=0,
        # "photos": ["string"],
        user_id=user["id"],
        quadrature=0,
        floor=0,
        address="string",
        is_active=True,
    )
    item = Flat(**data)
    repository = FlatRepository(session=db_session)
    await repository.add(item)
    return item.id
