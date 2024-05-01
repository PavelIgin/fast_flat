import logging
import os
from random import randint

import aioboto3
import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import env
from flat.models import Photo
from flat.repositories import PhotoRepository
from flat.schemas import PhotoCreateSchema
from users.models import User

env.read_env()
logger = logging.getLogger(__name__)


async def create_photo(
    item: PhotoCreateSchema, user: User, session: AsyncSession
):
    item_dict = item.dict()
    return await create_photo_and_s3_object(item_dict)


async def get_list_photo(session: AsyncSession):
    result = await session.execute(select(Photo))
    return result.scalars().all()


async def create_photo_and_s3_object(item_dict: dict):
    photo = item_dict["photo"]
    name_file = os.path.basename(photo)
    identify_number = str(randint(0, 99))
    key = identify_number + name_file
    async with aiohttp.ClientSession() as session:
        async with session.get(photo) as response:
            img = await response.content.read()
            async with aioboto3.Session().client(
                endpoint_url=env.str("ENDPOINT_URL", default="endponts"),
                service_name="s3",
                aws_access_key_id=env.str("AWS_ACCESS_KEY_ID", default="key"),
                aws_secret_access_key=env.str(
                    "AWS_SECRET_ACCESS_KEY", default="access_key"
                ),
            ) as client:
                await client.put_object(Bucket="fastflat", Key=key, Body=img)
    item_dict["photo"] = env.str("BUCKET_URL", default="bucket url") + key
    photo_instance = Photo(**item_dict)
    repository = PhotoRepository()
    await repository.add(photo_instance)
    return photo_instance
