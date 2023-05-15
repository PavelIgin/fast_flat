from typing import List

import uuid

from fastapi import APIRouter, Depends

from users.models import fastapi_user, User

from flat.schemas import FlatSchema, FlatCreate, FlatUpdate, FlatPrivateSchema, FlatPrivateInstanceSchema
from flat.service import create_flat, get_flat_list, get_flat_instance, update_flat, get_private_flats, \
    get_private_flat_instance
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


@app.get('/private', response_model=List[FlatPrivateSchema])
async def list_private(db: Session = Depends(get_db), user: User = Depends(current_user),):
    return await get_private_flats(db, user)


@app.get('/{pk}', response_model=FlatSchema)
async def get_flat_single(pk: uuid.UUID, db: Session = Depends(get_db)):
    return await get_flat_instance(pk, db)


@app.get('/private/{pk}', response_model=FlatPrivateInstanceSchema)
async def get_private_flat_single(pk: uuid.UUID, db: Session = Depends(get_db)):
    return await get_private_flat_instance(pk, db)


@app.patch('/{pk}', response_model=FlatUpdate)
async def flat_update(pk: uuid.UUID, item: FlatUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return await update_flat(pk, item, user, db)