from fastapi import FastAPI

from db import async_session

app = FastAPI()


async def get_session():
    session = async_session()
    try:
        yield session
    except BaseException:
        await session.rollback()
        raise
    finally:
        await session.close()
