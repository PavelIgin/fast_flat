import databases

from dependency_injector import providers

from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL_ASYNC = 'postgresql+asyncpg://postgres:gilsander1861@localhost/fast_flat'
DATABASE_URL_SYNC = 'postgresql://postgres:gilsander1861@localhost/fast_flat'
# TODO Переменные не должны быть прописаны в лоб, креды вынеси в .env
# TODO под переменные в принципе нужен отдельный
#  файл, какой-то класс или даже просто файл со списком переменных

databases = databases.Database(DATABASE_URL_ASYNC)

engine = providers.Singleton(
        create_async_engine,
        url=DATABASE_URL_SYNC
    )

engine_async = create_async_engine(DATABASE_URL_ASYNC)
