import asyncio
import typing as t

import pytest
from environs import Env
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
)

from base import Base
from db import DATABASE_URL_ASYNC, async_session
from main import app, engine

env = Env()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def db_connection() -> AsyncConnection:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    engine = create_async_engine(url=DATABASE_URL_ASYNC)
    conn = await engine.connect()
    conn = await conn.execution_options(autocommit=False)
    return conn


@pytest.fixture(scope="session")
async def db_session() -> AsyncSession:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    return async_session()


async def get_test_db_connection() -> AsyncConnection:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    engine = create_async_engine(url=DATABASE_URL_ASYNC)
    conn = await engine.connect()
    conn = await conn.execution_options(autocommit=False)
    return conn


@pytest.fixture(scope="session", autouse=True)
async def apply_migrations() -> t.AsyncGenerator[t.Any, t.Any]:
    print("apply migrations")
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
async def client() -> TestClient:
    client = TestClient(app=app)
    return client
