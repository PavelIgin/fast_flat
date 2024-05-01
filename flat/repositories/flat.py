from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload, selectinload, with_expression

from flat.models import Flat, Photo, Renting
from flat.schemas import FlatUpdate
from users.models import User

from .base import BaseRepository


class FlatRepository(BaseRepository):

    async def list_flat(self):
        return (
            await self.session.execute(
                select(Flat)
                .options(
                    joinedload(Flat.user),
                    joinedload(Flat.photos).load_only(Photo.photo),
                )
                .distinct()
            )
            .unique()
            .scalars()
            .all()
        )

    async def list_private(self):
        subq = select(Renting).subquery()
        stmt = (
            select(Flat, Flat.count_rentings)
            .group_by(Flat.id)
            .join(subq, Flat.id == subq.c.flat_id)
            .options(
                with_expression(
                    Flat.count_rentings,
                    func.count(subq.c.id).label("count_rentings"),
                ),
                joinedload(Flat.user),
                joinedload(Flat.photos).load_only(Photo.photo),
            )
            .distinct()
        )
        flats = await self.session.execute(stmt)
        return flats.unique().scalars().all()

    async def retrieve_private(self, pk: UUID):
        result = await self.session.execute(
            select(Flat)
            .where(Flat.id == pk)
            .options(
                selectinload(Flat.user),
                joinedload(Flat.photos).load_only(Photo.photo),
                joinedload(Flat.rentings),
            )
        )
        flat = result.scalar()
        return flat

    async def retrieve_flat(self, pk: UUID):
        result = await self.session.execute(
            select(Flat)
            .where(Flat.id == pk)
            .options(
                selectinload(Flat.user),
                joinedload(Flat.photos).load_only(Photo.photo),
            )
        )
        flat = result.scalar()
        return flat

    async def update_flat(self, pk: UUID, item: FlatUpdate, user: User):
        query = (
            update(Flat)
            .where(Flat.id == pk, Flat.user_id == user.id)
            .values(**item.dict())
            .returning(Flat.user_id)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar()
