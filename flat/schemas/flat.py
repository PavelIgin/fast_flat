from typing import Optional, List, Dict

from pydantic import BaseModel, UUID4, AnyUrl
from users.shemas import UserForFlat
from .photo import PhotoCreateSchema


class PhotoSchema(BaseModel):
    photo: AnyUrl
    id: UUID4

    class Config:
        orm_mode = True


class FlatSchema(BaseModel):
    id: UUID4
    cost: int
    photos: List[PhotoSchema] = None
    user: Optional[UserForFlat] = None
    quadrature: int = None
    floor: int = None
    address: str = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class FlatSchemaForRenting(BaseModel):
    id: UUID4
    cost: int
    address: str = None
    is_active: Optional[bool] = None

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
    photos: List[PhotoSchema] = None

    class Config:
        orm_mode = True


class FlatID(BaseModel):
    id: UUID4
