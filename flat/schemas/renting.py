import datetime
from typing import Any, Optional, Tuple, Type

from pydantic import UUID4, BaseModel, ValidationError

from flat.messages import upper_date_more_then_lower
from flat.schemas import FlatSchemaForRenting


class DateRange(BaseModel):
    start: Optional[datetime.date]
    end: Optional[datetime.date]

    def validate(cls: Type[datetime.date], value: Any):
        if value["start"] > value["end"]:
            raise ValidationError(detail=upper_date_more_then_lower)
        return value


class RentingSchema(BaseModel):
    id: UUID4
    date_range: Tuple[datetime.date, datetime.date]
    count_guest: int
    flat: FlatSchemaForRenting
    status: Optional[bool] = None

    class Config:
        orm_mode = True


class RentingCreate(BaseModel):
    #  id: UUID4
    lease_range: DateRange
    count_guest: int
    flat_id: UUID4

    class Config:
        orm_mode = True
