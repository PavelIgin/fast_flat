import datetime
from typing import Any, Optional, Tuple, Type

from pydantic import UUID4, BaseModel, ValidationError

from flat.messages import UPPER_DATE_MUST_BE_MORE_THEN_LOWER
from flat.schemas import FlatSchemaForRenting


class DateRange(BaseModel):
    start: Optional[datetime.date]
    end: Optional[datetime.date]

    def validate(cls: Type[datetime.date], value: Any):
        if value["start"] > value["end"]:
            raise ValidationError(detail=UPPER_DATE_MUST_BE_MORE_THEN_LOWER)
        return value


class RentingSchema(BaseModel):
    id: UUID4
    date_range: Tuple[datetime.date, datetime.date]
    count_guest: int
    flat: FlatSchemaForRenting
    status: Optional[bool] = None

    class Config:
        from_attributes = True


class RentingCreate(BaseModel):
    #  id: UUID4
    lease_range: DateRange
    count_guest: int
    flat_id: UUID4

    class Config:
        from_attributes = True
