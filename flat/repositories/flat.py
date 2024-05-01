from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload, selectinload, with_expression

from flat.models import Flat, Photo, Renting
from flat.schemas import FlatUpdate

from .base import BaseRepository


class FlatRepository(BaseRepository):

    async def list_flat(self):
        result = await self.session.execute(
            select(Flat)
            .options(
                joinedload(Flat.user),
                joinedload(Flat.photos).load_only(Photo.photo),
            )
            .distinct()
        )
        return result.unique().scalars().all()

    async def list_private(self, user):
        subq = select(Renting).subquery()
        stmt = (
            select(Flat, Flat.count_rentings)
            .group_by(Flat.id)
            .join(subq, Flat.id == subq.c.flat_id)
            .where(Flat.user_id == user.id)
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
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

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
        return result.scalar()

    async def retrieve_flat(self, pk: UUID):
        result = await self.session.execute(
            select(Flat)
            .where(Flat.id == pk)
            .options(
                selectinload(Flat.user),
                joinedload(Flat.photos).load_only(Photo.photo),
            )
        )
        return result.scalar()

    async def update_flat(self, pk: UUID, item: FlatUpdate):
        result = await self.session.execute(
            update(Flat)
            .where(Flat.id == pk)
            .values(**item.dict())
            .returning(Flat.user_id)
        )
        await self.session.commit()
        return result.scalar()
