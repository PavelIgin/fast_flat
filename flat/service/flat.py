from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from flat.models import Flat
from flat.schemas import FlatCreate, FlatUpdate
from users.service import check_user
from users.models import User
from db import engine_async


async def get_flat_list():
    async_session = sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as sessions:
        result = await sessions.execute(select(Flat).options(selectinload(Flat.user)))
        return result.scalars().all()


async def get_flat_instance(pk: UUID):
    async_session = sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as sessions:
        result = await sessions.execute(select(Flat).where(Flat.id == pk).options(selectinload(Flat.user)))
        return result.scalar()


async def update_flat(pk: UUID, item: FlatUpdate, user: User):
    """Обновить данные о квартире.
    Args:
        pk: UUID квартиры
        item: Форма с новыми данными о квартире
        user: Пользователь, выполняющий запрос

    Raises:
        NotFoundOrAccessDenied.

    Returns:
        Объект обновленной квартиры.
    """
    async_session = sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as sessions:
        query = update(Flat).where(
            Flat.id == pk,
            Flat.user_id == user.id
        ).values(**item.dict()).returning(Flat.user_id)
        result = await sessions.execute(query)
        if not result:
            # TODO перенести в messages.py
            raise Exception('Объект не найден или недоступен для редактирования.')
        await check_user(user, result)
        await sessions.commit()
        return result.scalar()


async def create_flat(item: FlatCreate, user: User):
    async_session = sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as sessions:
        item_dict = item.dict()
        item_dict['user_id'] = user.id
        flat_instance = Flat(**item_dict)
        sessions.add(flat_instance)
        await sessions.commit()
        return flat_instance
