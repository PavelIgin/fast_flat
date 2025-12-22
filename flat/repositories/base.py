from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, instance):
        self.session.add(instance)
        await self.session.commit()
