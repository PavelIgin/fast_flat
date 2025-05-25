from typing import Optional

from pydantic import UUID4, AnyUrl, BaseModel, Field


class PhotoSchema(BaseModel):
    id: UUID4
    flat: UUID4
    photo: AnyUrl
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class PhotoCreateSchema(BaseModel):
    photo: AnyUrl = Field(None, description="URL image")
    flat_id: UUID4

    class Config:
        from_attributes = True
