from uuid import UUID
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.orm import selectinload, joinedload, with_expression
from sqlalchemy import func

from flat.models import Flat, Photo, Renting
from flat.schemas import FlatCreate, FlatUpdate, FlatSchema
from .photo import create_photo_and_s3_object
from users.models import User

from sqlalchemy import inspect


async def get_flat_list(db: AsyncSession):
    result = await db.execute(select(Flat).
                              options(joinedload(Flat.user),
                                      joinedload(Flat.photos).load_only(Photo.photo)).distinct())
    flats = result.unique().scalars().all()
    return flats


async def get_private_flats(db: AsyncSession, user: User):
    subq = select(Renting).subquery()
    stmt = select(Flat,
                  Flat.count_rentings).group_by(Flat.id
                                                ).join(subq,
                                                       Flat.id == subq.c.flat_id).options(
        with_expression(Flat.count_rentings, func.count(subq.c.id).label('count_rentings')),
        joinedload(Flat.user),
        joinedload(Flat.photos).load_only(Photo.photo)).distinct()
    flats = await db.execute(stmt)
    return flats.unique().scalars().all()


async def get_private_flat_instance(pk: UUID, db: AsyncSession):
    result = await db.execute(select(Flat).where(Flat.id == pk).options(selectinload(Flat.user),
                                                                        joinedload(Flat.photos).load_only(Photo.photo),
                                                                        joinedload(Flat.rentings)))
    flat = result.scalar()
    return flat


async def get_flat_instance(pk: UUID, db: AsyncSession):
    result = await db.execute(select(Flat).where(Flat.id == pk).options(selectinload(Flat.user),
                                                                        joinedload(Flat.photos).load_only(Photo.photo)))
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
    dict_item = object_as_dict(flat_instance)
    if photo_list:
        list_tasks = []
        saved_photos = []
        for photo in photo_list:
            item_dict_photo = {'photo': photo, 'flat_id': flat_instance.id}
            task = asyncio.create_task(create_photo_and_s3_object(item_dict_photo))
            list_tasks.append(task)
        photos_gather = await asyncio.gather(*list_tasks)
        for photo in photos_gather:
            saved_photos.append({'id': photo.id, 'photo': photo.photo})
        dict_item['photos'] = saved_photos
    flat_serializer = FlatSchema(**dict_item)
    return flat_serializer


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
