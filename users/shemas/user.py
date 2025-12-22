import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserForFlat(BaseModel):
    email: EmailStr
    telegram_contact: Optional[str]

    class Config:
        from_attributes = True


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    telegram_contact: str = None


class UserUpdate(schemas.BaseUserUpdate):
    telegram_contact: str = None
