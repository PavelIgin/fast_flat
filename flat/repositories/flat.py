from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload, selectinload, with_expression

from flat.models import Flat, Photo, Promotion, Renting
from flat.schemas import FlatUpdate
from flat.enums import PromotionEnum

from .base import BaseRepository


class FlatRepository(BaseRepository):

    @staticmethod
    def get_type_promotion():
        return func.coalesce(
            select(Promotion.type)
            .where(Promotion.flat_id == Flat.id)
            .order_by(Promotion.start.desc())
            .limit(1),
            PromotionEnum.DEFAULT,
        ).label("type_promotion")

    async def list_flat(self):
        type_promotion = self.get_type_promotion()
        query = await self.session.execute(
            select(
                Flat,
            )
            .options(
                joinedload(Flat.user),
                joinedload(Flat.photos),
                with_expression(
                    Flat.type_promotion,
                    type_promotion,
                ),
            )
            .order_by(type_promotion.desc())
        )
        result = query.unique().scalars().all()
        return result

    async def list_private(self, user):
        type_promotion = self.get_type_promotion()
        stmt = (
            select(Flat, Flat.count_rentings)
            .group_by(Flat.id)
            .outerjoin(Renting, Flat.id == Renting.flat_id)
            .where(Flat.user_id == user.id)
            .options(
                with_expression(
                    Flat.count_rentings,
                    func.count(Renting.flat_id).label("count_rentings"),
                ),
                with_expression(
                    Flat.type_promotion,
                    type_promotion,
                ),
                joinedload(Flat.user),
                joinedload(Flat.photos).load_only(Photo.photo),
            )
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def retrieve_private(self, pk: UUID):
        type_promotion = self.get_type_promotion()
        result = await self.session.execute(
            select(Flat)
            .where(Flat.id == pk)
            .options(
                selectinload(Flat.user),
                joinedload(Flat.photos).load_only(Photo.photo),
                joinedload(Flat.rentings),
                with_expression(
                    Flat.type_promotion,
                    type_promotion,
                ),
            )
        )
        return result.scalar()

    async def retrieve_flat(self, pk: UUID):
        type_promotion = self.get_type_promotion()
        result = await self.session.execute(
            select(Flat)
            .where(Flat.id == pk)
            .options(
                selectinload(Flat.user),
                joinedload(Flat.photos).load_only(Photo.photo),
                with_expression(
                    Flat.type_promotion,
                    type_promotion,
                ),
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
