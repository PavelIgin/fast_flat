import uuid
from sqlalchemy import select, exists
from fastapi import HTTPException

from flat.models import Renting, Flat
from users.models import User


async def check_flat_owner(pk: uuid.UUID, user: User, sessions):
    rent_query = select(Renting).where(Renting.id == pk).join(Renting.flat)
    rent_instance = await sessions.execute(rent_query)
    instance = select(Flat).where(select(Flat).where(Flat.id == rent_instance.scalar().flat_id, Flat.user_id == user.id).exists())
    result = await sessions.execute(instance)
    if result.scalar():
        return True
    else:
        raise HTTPException(status_code=404, detail='Item Not Found')