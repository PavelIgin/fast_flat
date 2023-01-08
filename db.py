import databases

from dependency_injector import providers

from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL_ASYNC = 'postgresql+asyncpg://postgres:gilsander1861@localhost/fast_flat'
DATABASE_URL_SYNC = 'postgresql://postgres:gilsander1861@localhost/fast_flat'

databases = databases.Database(DATABASE_URL_ASYNC)

engine = providers.Singleton(
        create_async_engine,
        url=DATABASE_URL_SYNC
    )

engine_async = create_async_engine(DATABASE_URL_ASYNC)
