import uuid
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from flat.models import Renting
from flat.repositories import RentingRepository
from flat.schemas import RentingCreate
from users.models import User


async def list_renting_service(user: User, session: AsyncSession):
    repository = RentingRepository(session=session)
    result = await repository.list_renting(user)
    return result


async def create_renting_service(
    item: RentingCreate, user: User, session: AsyncSession
):
    item_dict = item.model_dump()
    item_dict["user_id"] = user.id
    # todo понять что делать
    item_dict["lease_range"] = [
        item_dict["lease_range"]["start"],
        item_dict["lease_range"]["end"],
    ]
    repository = RentingRepository(session=session)
    result = await repository.get_free_dates(item_dict)
    if result.scalar():
        raise HTTPException(status_code=400, detail="DATE_ALREADY_RENTED")
    item_dict["status"] = None
    renting_instance = Renting(**item_dict)
    await repository.add(renting_instance)
    return renting_instance


async def renting_approve_service(pk: uuid.UUID, user, session: AsyncSession):
    repository = RentingRepository(session=session)
    result = await repository.check_flat_owner(pk, user)
    if result.scalar():
        await repository.renting_approve(pk)
    else:
        raise HTTPException(status_code=404, detail="ITEM_NOT_FOUND")


async def renting_cancel_service(pk: uuid.UUID, user, session: AsyncSession):
    repository = RentingRepository(session=session)
    result = await repository.check_flat_owner(pk, user)
    if result.scalar():
        await repository.renting_cancel(pk)
    else:
        raise HTTPException(status_code=404, detail="ITEM_NOT_FOUND")


async def check_date_is_free(session: AsyncSession, item_dict):
    item_dict["lease_range"][0] = item_dict["lease_range"][0] + timedelta(
        days=1
    )
    repository = RentingRepository(session=session)
    result = await repository.get_free_dates(item_dict)
    if result.scalar():
        return False
    else:
        item_dict["lease_range"][0] = item_dict["lease_range"][0] - timedelta(
            days=1
        )
        return True
