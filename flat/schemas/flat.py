import datetime
from typing import List, Optional

from pydantic import UUID4, AnyUrl, BaseModel

from users.shemas import UserForFlat


class LeaseRangeSchema(BaseModel):

    lower: datetime.date = None
    upper: datetime.date = None

    class Config:
        orm_mode = True


class RentingSchema(BaseModel):
    id: UUID4
    lease_range: LeaseRangeSchema
    count_guest: int
    status: Optional[bool] = None

    class Config:
        orm_mode = True


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


class FlatPrivateSchema(BaseModel):
    id: UUID4
    cost: int
    count_rentings: int
    photos: List[PhotoSchema] = None
    user: Optional[UserForFlat] = None
    quadrature: int = None
    floor: int = None
    address: str = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class FlatPrivateInstanceSchema(BaseModel):
    id: UUID4
    cost: int
    # count_rentings: int
    rentings: List[RentingSchema] = None
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


class FlatUpdate(FlatSchema):

    id: UUID4
    cost: int
    quadrature: int = None
    floor: int = None
    address: str = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class FlatCreate(BaseModel):

    cost: int
    quadrature: int = None
    floor: int = None
    address: str = None
    is_active: Optional[bool] = None

    photos: List[str] = None

    class Config:
        orm_mode = True


class FlatID(BaseModel):
    id: UUID4
