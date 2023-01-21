from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from db import engine_async
from base import Base
from sqlalchemy import Column, String


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = 'user'

    username = Column(String)


# TODO управлению сессиями БД нужен отдельный файл - и не в каком-то
#  конкретном приложении, а мб даже в корне. Например, создать папку core для общих вещей
#  /users
#  /flats
#  /core


async_session_maker = sessionmaker(engine_async, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
