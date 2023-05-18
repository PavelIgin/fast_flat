import uuid

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.datetime_parse import parse_date
from flat.models import Renting, Flat
from flat.schemas import RentingCreate
from flat.permissions import check_flat_owner

from users.models import User
from sqlalchemy.sql.expression import exists
from datetime import timedelta


async def list_renting(user: User, db: AsyncSession):
    result = await db.execute(
        select(Renting).where(Renting.user_id == user.id)
        .options(joinedload(Renting.user)).
        options(joinedload(Renting.flat).joinedload(Flat.user)))
    return result.scalars().all()


async def create_renting(item: RentingCreate, user: User, db: AsyncSession):
    item_dict = item.dict()
    item_dict['user_id'] = user.id
    item_dict['lease_range'] = [parse_date(item_dict['lease_range']['start']),
                                parse_date(item_dict['lease_range']['end'])]
    if not await check_date_is_free(db, item_dict):
        raise 'date already rented'
    item_dict['status'] = None
    renting_instance = Renting(**item_dict)
    db.add(renting_instance)
    await db.commit()
    return renting_instance


async def renting_approve(pk: uuid.UUID, user, db: AsyncSession):
    await check_flat_owner(pk, user, db)
    instance = update(Renting).where(Renting.id == pk).values(status=True)
    await db.execute(instance)
    await db.commit()


async def renting_cancel(pk: uuid.UUID, user, db: AsyncSession):
    await check_flat_owner(pk, user, db)
    instance = update(Renting).where(Renting.id == pk).values(status=False)
    await db.execute(instance)
    await db.commit()


async def user_is_owner(pk: uuid.UUID, user: User, sessions):
    rent_query = select(Renting).where(Renting.id == pk).join(Renting.flat)
    rent_instance = await sessions.execute(rent_query)
    instance = select(Flat).where(Flat.id == rent_instance.scalar().flat_id, Flat.user_id == user.id)
    result = await sessions.execute(instance)
    if result:
        return True


async def check_date_is_free(db: AsyncSession, item_dict):
    item_dict['lease_range'][0] = item_dict['lease_range'][0] + timedelta(days=1)
    queryset = await \
        db.execute(select(exists(Renting)).filter(Renting.flat_id == item_dict['flat_id'], Renting.lease_range.overlaps(
        item_dict['lease_range'])))
    if queryset.scalar():
        return False
    else:
        item_dict['lease_range'][0] = item_dict['lease_range'][0] - timedelta(days=1)
        return True
