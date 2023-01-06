import sqlalchemy
import databases

from dependency_injector import providers

from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = 'postgresql+asyncpg://postgres:gilsander1861@host:5432/fast_flat'

databases = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = providers.Singleton(
        create_async_engine,
        url=DATABASE_URL
    )
