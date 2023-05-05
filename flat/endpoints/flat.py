from typing import List

import uuid

from fastapi import APIRouter, Depends

from users.models import fastapi_user, User

from flat.schemas import FlatSchema, FlatCreate, FlatUpdate
from flat.service import create_flat, get_flat_list, get_flat_instance, update_flat, get_private_flats
from sqlalchemy.orm import Session
from core.db import get_db
current_user = fastapi_user.current_user()

app = APIRouter()


@app.post('', response_model=FlatSchema)
async def post_flat(item: FlatCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return await create_flat(item, user, db)


@app.get('', response_model=List[FlatSchema])
async def get_flat(db: Session = Depends(get_db)):
    return await get_flat_list(db)


@app.get('/get_private_flat', response_model=List[FlatSchema])
async def get_private_flat(db: Session = Depends(get_db), user: User = Depends(current_user),):
    return await get_private_flats(db, user)


@app.get('/{pk}', response_model=FlatSchema)
async def get_flat_single(pk: uuid.UUID, db: Session = Depends(get_db)):
    return await get_flat_instance(pk, db)


@app.patch('/{pk}')
async def flat_update(pk: uuid.UUID, item: FlatUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return await update_flat(pk, item, user, db)