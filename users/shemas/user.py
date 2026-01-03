from typing import Optional

from fastapi_users import schemas, models
from pydantic import BaseModel, EmailStr, ConfigDict


class UserForFlat(BaseModel):
    email: EmailStr
    telegram_contact: Optional[str]

    class Config:
        from_attributes = True


class UserRead(schemas.CreateUpdateDictModel):
    id: models.ID
    telegram_contact: str = None
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.CreateUpdateDictModel):
    telegram_contact: str = None
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(schemas.CreateUpdateDictModel):
    telegram_contact: str = None
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
