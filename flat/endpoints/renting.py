import uuid

from typing import List

from fastapi import APIRouter, Depends

from users.models import fastapi_user, User

from flat.schemas import RentingCreate, RentingIdSchema, RentingSchema
from flat.service import create_renting, get_renting, renting_approve

current_user = fastapi_user.current_user()

app = APIRouter()


@app.post('')
async def renting_create(item: RentingCreate, user: User = Depends(current_user)):
    return await create_renting(item, user)


@app.get('', response_model=List[RentingSchema])
async def renting_get(user: User = Depends(current_user)):
    return await get_renting(user)


@app.patch('/approve')
async def approve_renting(pk: uuid.UUID, user: User = Depends(current_user)):
    return await renting_approve(pk, user)
