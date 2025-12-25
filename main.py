from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqladmin import Admin
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from admin import PhotoAdmin
from admin.flat import FlatAdmin
from core.jwt import auth_backend
from db import DATABASE_URL_SYNC
from flat.endpoints import flat, photo, renting
from users.models import fastapi_user
from users.shemas import UserCreate, UserRead

Base = declarative_base()
engine = create_engine(DATABASE_URL_SYNC)
app = FastAPI()
current_user = fastapi_user.current_user()

app.include_router(flat.app, prefix="/api/v1/flat", tags=["flat"])
app.include_router(renting.app, prefix="/api/v1/renting", tags=["renting"])
app.include_router(photo.app, prefix="/api/v1/photo", tags=["photo"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    fastapi_user.get_auth_router(auth_backend),
    prefix="/api/v1/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_user.get_register_router(UserRead, UserCreate),
    prefix="/api/v1/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_user.get_reset_password_router(),
    prefix="/api/v1/auth",
    tags=["auth"],
)

admin = Admin(app, engine)
admin.add_view(FlatAdmin)
admin.add_view(PhotoAdmin)
