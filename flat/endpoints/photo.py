from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.db import get_session
from flat.schemas import PhotoCreateSchema, PhotoSchema
from flat.service import create_photo
from users.models import User, fastapi_user

current_user = fastapi_user.current_user()

app = APIRouter()


@app.post("", response_model=PhotoSchema)
async def post_photo(
    item: PhotoCreateSchema,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    return await create_photo(item, user, session)
