from fastapi import FastAPI
from db import async_session


app = FastAPI()


async def get_db():
    db = async_session()
    try:
        yield db
    except:
        await db.rollback()
        raise
    finally:
        await db.close()
