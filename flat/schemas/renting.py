import datetime

from typing import Type, Any, Optional, List, Tuple
from psycopg2.extras import DateRange as DATERANGE
from fastapi import HTTPException, status
from pydantic import BaseModel, UUID4
from asyncpg.types import Range
from flat.schemas import FlatSchema
from psycopg2.extras import DateTimeRange


class DateRange(BaseModel):
    from_: Optional[datetime.date]
    to_: Optional[datetime.date]

    def validate(cls: Type[datetime.date], value: Any):
        if value['from_'] > value['to_']:
            raise HTTPException(detail='upper date must be more then lower', status_code=status.HTTP_400_BAD_REQUEST)
        return value


class RentingSchema(BaseModel):
    id: UUID4
    date_range: Tuple[datetime.date, datetime.date]
    count_guest: int
    flat: FlatSchema
    is_approved: bool

    class Config:
        orm_mode = True


class RentingIdSchema(BaseModel):
    id: UUID4

    class Config:
        orm_mode = True


class RentingCreate(BaseModel):
    #  id: UUID4
    lease_range: DateRange
    count_guest: int
    flat_id: UUID4

    class Config:
        orm_mode = True
