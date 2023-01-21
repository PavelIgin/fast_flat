import uuid

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserForFlat(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
