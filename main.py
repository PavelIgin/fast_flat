from fastapi import FastAPI

from core.jwt import auth_backend
from users.models import fastapi_user
from users.shemas import UserCreate, UserRead
from flat.endpoints import flat, renting, photo
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

current_user = fastapi_user.current_user()

app.include_router(flat.app, prefix='/flat')
app.include_router(renting.app, prefix='/renting')
app.include_router(photo.app, prefix='/photo')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

