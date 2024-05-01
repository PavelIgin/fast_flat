import os

from dependency_injector import providers
from environs import Env
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

env_file = os.path.join(".env")
env = Env()
env.read_env()
DATABASE_URL_ASYNC = env.str(
    "DATABASE_URL_ASYNC", default="DATABASE_URL_ASYNC"
)
DATABASE_URL_SYNC = env.str("DATABASE_URL_SYNC", default="DATABASE_URL_SYNC")

engine = providers.Singleton(create_async_engine, url=DATABASE_URL_SYNC)

engine_async = create_async_engine(
    DATABASE_URL_ASYNC, future=True, echo=True, poolclass=NullPool
)
async_session = sessionmaker(
    engine_async, expire_on_commit=False, class_=AsyncSession
)
