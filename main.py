from fastapi import FastAPI

from users.models import fastapi_user, auth_backend

from users.shemas import UserCreate, UserRead

app = FastAPI()


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
