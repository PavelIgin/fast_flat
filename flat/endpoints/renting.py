import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.db import get_session
from flat.schemas import RentingCreate, RentingSchema
from flat.service import (
    create_renting_service,
    list_renting_service,
    renting_approve_service,
    renting_cancel_service,
)
from users.models import User, fastapi_user

current_user = fastapi_user.current_user()

app = APIRouter()


@app.post("")
async def create_renting(
    item: RentingCreate,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
    status_code=status.HTTP_201_CREATED,
):
    return await create_renting_service(item, user, session)


@app.get("/private", response_model=List[RentingSchema])
async def list_renting(
    user: User = Depends(current_user), session: Session = Depends(get_session)
):
    return await list_renting_service(user, session)


@app.patch("/approve/{pk}/")
async def approve_renting(
    pk: uuid.UUID,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    return await renting_approve_service(pk, user, session)


@app.patch("/cancel/{pk}/")
async def cancel_renting(
    pk: uuid.UUID,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    return await renting_cancel_service(pk, user, session)
