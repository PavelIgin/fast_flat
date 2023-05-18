import uuid

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from users.models import fastapi_user, User

from flat.schemas import RentingCreate, RentingSchema
from flat.service import create_renting, list_renting, renting_approve, renting_cancel
from core.db import get_db

current_user = fastapi_user.current_user()

app = APIRouter()


@app.post('')
async def renting_create(item: RentingCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return await create_renting(item, user, db)


@app.get('/private', response_model=List[RentingSchema])
async def renting_get(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return await list_renting(user, db)


@app.patch('/approve/{pk}/')
async def approve_renting(pk: uuid.UUID, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return await renting_approve(pk, user, db)


@app.patch('/cancel/{pk}/')
async def cancel_renting(pk: uuid.UUID, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return await renting_cancel(pk, user, db)