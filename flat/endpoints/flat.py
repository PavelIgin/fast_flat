import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.db import get_session
from flat.schemas import (
    FlatCreate,
    FlatPrivateInstanceSchema,
    FlatPrivateSchema,
    FlatSchema,
    FlatUpdate,
)
from flat.service import (
    list_flat_service,
    list_private_service,
    post_flat_service,
    retrieve_flat_service,
    retrieve_private_service,
    update_flat_service,
)
from users.models import User, fastapi_user

current_user = fastapi_user.current_user()

app = APIRouter()


@app.post("", response_model=FlatSchema)
async def post_flat(
    item: FlatCreate,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    return await post_flat_service(item, user, session)


@app.get("", response_model=List[FlatSchema])
async def list_flat(session: Session = Depends(get_session)):
    return await list_flat_service(session)


@app.get("/private", response_model=List[FlatPrivateSchema])
async def list_private(
    session: Session = Depends(get_session()),
    user: User = Depends(current_user),
):
    return await list_private_service(session, user)


@app.get("/{pk}", response_model=FlatSchema)
async def retrieve_flat(
    pk: uuid.UUID, session: Session = Depends(get_session)
):
    return await retrieve_flat_service(pk, session)


@app.get("/private/{pk}", response_model=FlatPrivateInstanceSchema)
async def retrieve_private(
    pk: uuid.UUID, session: Session = Depends(get_session)
):
    return await retrieve_private_service(pk, session)


@app.patch("/{pk}", response_model=FlatUpdate)
async def update_flat(
    pk: uuid.UUID,
    item: FlatUpdate,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    return await update_flat_service(pk, item, user, session)
