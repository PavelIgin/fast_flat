from db import async_session


class PhotoRepository:

    async def add(self, photo_instance):
        async with async_session() as session:
            session.add(photo_instance)
            await session.commit()
