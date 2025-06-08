import datetime

import pytest
from repositories import RentingRepository

from flat.models import Renting

__all__ = ("base_renting",)


@pytest.fixture
async def base_renting(db_session, flat, user):
    rent = Renting(
        user_id=user["id"],
        flat_id=flat,
        lease_range=[
            (datetime.datetime.now() - datetime.timedelta(days=1)).date(),
            (datetime.datetime.now() + datetime.timedelta(days=1)).date(),
        ],
        count_guest=1,
    )
    await RentingRepository(session=db_session).add(rent)
    return rent.id
