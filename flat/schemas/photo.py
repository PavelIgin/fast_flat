from typing import Optional
from pydantic import BaseModel, UUID4, AnyUrl


class PhotoSchema(BaseModel):
    id: UUID4
    flat: UUID4
    photo: AnyUrl
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class PhotoCreateSchema(BaseModel):
    photo: AnyUrl
    flat_id: UUID4

    class Config:
        orm_mode = True
