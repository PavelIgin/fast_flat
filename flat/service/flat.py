from uuid import UUID
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.orm.attributes import set_committed_value
from sqlalchemy import select

from flat.models import Flat, Photo
from flat.schemas import FlatCreate, FlatUpdate
from .photo import create_photo_and_s3_object
from users.models import User


async def get_flat_list(db: AsyncSession):
    result = await db.execute(select(Flat).
                              options(joinedload(Flat.user),
                                      joinedload(Flat.photos).load_only(Photo.photo)).distinct())
    flats = result.unique().scalars().all()
    return flats


async def get_flat_instance(pk: UUID, db: AsyncSession):
    result = await db.execute(select(Flat).where(Flat.id == pk).options(selectinload(Flat.user),
                                                                        joinedload(Flat.photos).load_only('photo')))
    flat = result.scalar()
    return flat


async def update_flat(pk: UUID, item: FlatUpdate, user: User, db: AsyncSession):
    query = update(Flat).where(Flat.id == pk, Flat.user_id == user.id).values(**item.dict()).returning(Flat.user_id)
    result = await db.execute(query)
    await db.commit()
    return result.scalar()


async def create_flat(item: FlatCreate, user: User, db: AsyncSession):
    item_dict = item.dict()
    item_dict['user_id'] = user.id
    photo_list = item_dict.pop('photos')
    flat_instance = Flat(**item_dict)
    db.add(flat_instance)
    await db.commit()
    if photo_list:
        list_tasks = []
        for photo in photo_list:
            item_dict_photo = {'photo': photo, 'flat_id': flat_instance.id}
            task = asyncio.create_task(create_photo_and_s3_object(item_dict_photo))
            list_tasks.append(task)
        await asyncio.gather(*list_tasks)
    return flat_instance
