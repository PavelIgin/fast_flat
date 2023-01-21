from typing import List

import uuid

from fastapi import APIRouter, Depends

from users.models import fastapi_user, User

from flat.schemas import FlatSchema, FlatCreate, FlatUpdate
from flat.service import create_flat, get_flat_list, get_flat_instance, update_flat

current_user = fastapi_user.current_user()

app = APIRouter()


@app.post('')
async def post_flat(item: FlatCreate, user: User = Depends(current_user)):
    return await create_flat(item, user)


@app.get('', response_model=List[FlatSchema])
async def get_flat():
    return await get_flat_list()


@app.get('/{pk}', response_model=FlatSchema)
async def get_flat_single(pk: uuid.UUID):
    return await get_flat_instance(pk)


@app.patch('/{pk}')
async def flat_update(pk: uuid.UUID, item: FlatUpdate, user: User = Depends(current_user)):
    return await update_flat(pk, item, user)