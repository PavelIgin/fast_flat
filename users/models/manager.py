import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin

from core.jwt import SECRET, auth_backend
from core.user import get_user_db

from .user import User


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_user = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
