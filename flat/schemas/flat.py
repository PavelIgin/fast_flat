from typing import Optional

from pydantic import BaseModel, UUID4
from users.shemas import UserForFlat


class FlatSchema(BaseModel):
    id: UUID4
    cost: int
    user: Optional[UserForFlat] = None
    is_active: bool

    class Config:
        orm_mode = True


class FlatUpdate(BaseModel):
    cost: int
    is_active: bool

    class Config:
        orm_mode = True


class FlatCreate(BaseModel):
    cost: int
    is_active: bool

    class Config:
        orm_mode = True

