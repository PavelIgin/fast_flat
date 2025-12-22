import uuid

from sqlalchemy import exists, select, update
from sqlalchemy.orm import joinedload

from flat.models import Flat, Renting
from users.models import User

from .base import BaseRepository


class RentingRepository(BaseRepository):

    async def list_renting(self, user: User):
        result = await self.session.execute(
            select(Renting)
            .where(Renting.user_id == user.id)
            .options(joinedload(Renting.user))
            .options(joinedload(Renting.flat).joinedload(Flat.user))
        )
        return result.scalars().all()

    async def renting_approve(self, pk: uuid.UUID):
        instance = update(Renting).where(Renting.id == pk).values(status=True)
        await self.session.execute(instance)
        await self.session.commit()

    async def renting_cancel(self, pk):
        instance = update(Renting).where(Renting.id == pk).values(status=False)
        await self.session.execute(instance)
        await self.session.commit()

    async def check_flat_owner(self, pk: uuid.UUID, user: User):
        rent_query = select(Renting).where(Renting.id == pk).join(Renting.flat)
        rent_instance = await self.session.execute(rent_query)
        instance = select(Flat).where(
            select(Flat)
            .where(
                Flat.id == rent_instance.scalar().flat_id,
                Flat.user_id == user.id,
            )
            .exists()
        )
        result = await self.session.execute(instance)
        return result

    async def get_free_dates(self, item_dict):
        # todo занятые даты
        # todo переименовать в медод получения аренд пересекающихся с данными ввода
        result = await self.session.execute(
            select(exists(Renting)).filter(
                Renting.flat_id == item_dict["flat_id"],
                Renting.lease_range.overlaps(item_dict["lease_range"]),
            )
        )
        return result
