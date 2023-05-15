from fastapi import APIRouter, Depends

from users.models import fastapi_user, User

from flat.schemas import PhotoCreateSchema, PhotoSchema
from flat.service import create_photo
from sqlalchemy.orm import Session
from core.db import get_db
current_user = fastapi_user.current_user()

app = APIRouter()


@app.post('', response_model=PhotoSchema)
async def post_photo(item: PhotoCreateSchema, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return await create_photo(item, user, db)
