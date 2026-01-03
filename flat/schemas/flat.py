import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import UUID4, AnyUrl, BaseModel, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from flat.enums import PromotionEnum
from flat.models import Flat

from users.shemas import UserForFlat


class LeaseRangeSchema(BaseModel):

    lower: datetime.date = None
    upper: datetime.date = None

    class Config:
        from_attributes = True


class RentingSchema(BaseModel):
    id: UUID4
    lease_range: LeaseRangeSchema
    count_guest: int
    status: Optional[bool] = None

    class Config:
        from_attributes = True


class Photoschema(BaseModel):
    photo: AnyUrl
    id: UUID4

    class Config:
        from_attributes = True


class FlatSchema(BaseModel):
    id: UUID4
    cost: int
    #photos: List[#photoschema] = None
    user: Optional[UserForFlat]
    quadrature: Optional[int]
    floor: Optional[int]
    address: Optional[str]
    is_active: Optional[bool]
    type_promotion: int

    class Config:
        from_attributes = True


class FlatPrivateSchema(BaseModel):
    id: UUID4
    cost: int
    count_rentings: Optional[int]
    ##photos: Optional[List[#photoschema]] = None # todo доделать
    quadrature: Optional[int]
    floor: Optional[int]
    address: Optional[str]
    is_active: Optional[bool]
    type_promotion: Optional[int] = PromotionEnum.DEFAULT

    class Config:
        from_attributes = True


class FlatPrivateInstanceSchema(BaseModel):
    id: UUID4
    cost: int
    # count_rentings: int
    rentings: List[RentingSchema] = None
    #photos: List[#photoschema] = None
    user: Optional[UserForFlat]
    quadrature: Optional[int]
    floor: Optional[int]
    address: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_attributes = True


class FlatSchemaForRenting(BaseModel):
    id: UUID4
    cost: int
    address: str = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class FlatUpdate(BaseModel):

    cost: int
    quadrature: int = None
    floor: int = None
    address: str = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class FlatCreate(BaseModel):

    cost: int
    quadrature: int = None
    floor: int = None
    address: str = None
    is_active: Optional[bool] = None

    #photos: List[str] = None

    class Config:
        from_attributes = True


class FlatID(BaseModel):
    id: UUID4


class FlatFilter(Filter):
    __tablename__ = "flat"
    cost__gte: Optional[int] = None
    cost__lte: Optional[int] = None
    floor__gte: Optional[int] = None
    floor__lte: Optional[int] = None

    order_by: Optional[list[str]] = None
    class Constants(Filter.Constants):
        model = Flat


class FlatErrorMessage(BaseModel):
    detail: str = 'FLAT_DOES_NOT_EXISTS_BY_USER'
