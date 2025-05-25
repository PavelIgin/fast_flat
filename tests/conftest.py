import asyncio
import typing as t

import pytest
from asyncpg.exceptions import DuplicateDatabaseError, InvalidCatalogNameError
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, ProgrammingError
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from alembic import command
from alembic.config import Config
from db import DATABASE_URL_ASYNC
from main import app
from tests.fixtures import *


@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
async def db_connection() -> AsyncConnection:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    engine = create_async_engine(url=DATABASE_URL_ASYNC)
    conn = await engine.connect()
    conn = await conn.execution_options(autocommit=False)
    return conn


async def get_test_db_connection() -> AsyncConnection:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    engine = create_async_engine(url=DATABASE_URL_ASYNC)
    conn = await engine.connect()
    conn = await conn.execution_options(autocommit=False)
    return conn


async def drop_db() -> None:
    conn = await get_test_db_connection()
    try:
        await conn.execute(text("ROLLBACK"))
        await conn.execute(text(f"DROP DATABASE fast_flat_test"))
        print("SQL test database dropped")
    except (DBAPIError, InvalidCatalogNameError):
        await conn.execute(text("ROLLBACK"))


async def create_db() -> None:
    conn = await get_test_db_connection()
    await conn.execute(text("ROLLBACK"))
    try:
        await conn.execute(text(f"CREATE DATABASE fast_flat_test"))
    except (ProgrammingError, DuplicateDatabaseError):
        await conn.execute(text("ROLLBACK"))
    await conn.close()


@pytest.fixture()
async def apply_migrations() -> t.AsyncGenerator[t.Any, t.Any]:
    print("apply migrations")
    await create_db()
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")
    await drop_db()


@pytest.fixture
async def client(apply_migrations: None) -> TestClient:
    client = TestClient(app=app)
    return client
