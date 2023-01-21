from fastapi import FastAPI

from users.models import fastapi_user, auth_backend
from db import databases
from users.shemas import UserCreate, UserRead
from flat.endpoints import flat, renting

app = FastAPI()

current_user = fastapi_user.current_user()


@app.on_event('startup')
async def startup():
    await databases.connect()


@app.on_event('shutdown')
async def shutdown():
    await databases.disconnect()


app.include_router(flat.app, prefix='/flat')
app.include_router(renting.app, prefix='/renting')

app.include_router(
    fastapi_user.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_user.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
