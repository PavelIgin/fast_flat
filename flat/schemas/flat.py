from typing import Optional

from pydantic import BaseModel, UUID4
from users.shemas import UserForFlat


class FlatSchema(BaseModel):
    id: UUID4
    cost: int

    # TODO почему None может быть?
    user: Optional[UserForFlat] = None

    # TODO is_active может быть None
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

