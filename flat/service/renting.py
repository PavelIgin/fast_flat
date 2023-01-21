import uuid

from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.datetime_parse import parse_date
from flat.models import Renting, Flat
from flat.schemas import RentingCreate
from users.models import User
from db import engine_async


async def get_renting(user: User):
    async_session = sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as sessions:
        result = await sessions.execute(
            select(Renting).where(Renting.user_id == user.id)
            .options(joinedload(Renting.user)).
            options(joinedload(Renting.flat).joinedload(Flat.user)))
        return result.scalars().all()


async def create_renting(item: RentingCreate, user: User):
    async_session = sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as sessions:
        item_dict = item.dict()
        item_dict['user_id'] = user.id
        item_dict['lease_range'] = [parse_date(item_dict['lease_range']['from_']),
                                    parse_date(item_dict['lease_range']['to_'])]
        if not await check_date_is_free(sessions, item_dict):
            raise 'sdfsdf'
        renting_instance = Renting(**item_dict)
        sessions.add(renting_instance)
        await sessions.commit()
        return renting_instance


async def renting_approve(pk: uuid.UUID, user):
    async_session = sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as sessions:
        if not await user_is_owner(pk, user, sessions):
            raise 'user is not owner'
        instance = update(Renting).where(Renting.id == pk).values(is_approved=True)
        await sessions.execute(instance)
        await sessions.commit()


async def user_is_owner(pk: uuid.UUID, user: User, sessions):
    rent_query = select(Renting).where(Renting.id == pk).join(Renting.flat)
    rent_instance = await sessions.execute(rent_query)
    instance = select(Flat).where(Flat.id == rent_instance.scalar().flat_id, Flat.user_id == user.id)
    result = await sessions.execute(instance)
    if result:
        return True


async def check_date_is_free(sessions: AsyncSession, item_dict):
    queryset = select(Renting).filter(Renting.flat_id == item_dict['flat_id']).filter(Renting.lease_range.overlaps(
        item_dict['lease_range']))
    result = await sessions.execute(queryset)
    if result:
        return False
    else:
        return True
