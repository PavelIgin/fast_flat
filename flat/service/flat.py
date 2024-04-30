import os
import json
import pika
import asyncio

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.orm import selectinload, joinedload, with_expression
from sqlalchemy import func
from environs import Env

from flat.models import Flat, Photo, Renting
from flat.schemas import FlatCreate, FlatUpdate, FlatSchema
from flat.repositories import FlatRepository
from .photo import create_photo_and_s3_object
from users.models import User

from sqlalchemy import inspect

env_file = os.path.join('.env')
env = Env()
env.read_env()

RABBITMQ_HOST = env.str('RABBITMQ_HOST',
                        default='RABBITMQ_HOST')
RABBITMQ_USERNAME = env.str('RABBITMQ_USERNAME',
                            default='RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = env.str('RABBITMQ_PASSWORD',
                            default='RABBITMQ_PASSWORD')
# TODO ВЫЯСНИТЬ КУДА ОБЪЯВИТЬ ВСЕ ЭНВЫ


async def list_flat_service(session: AsyncSession):
    repository = FlatRepository(session=session)
    result = await repository.list_flat()
    return result


async def list_private_service(session: AsyncSession):
    repository = FlatRepository(session=session)
    result = await repository.list_private()
    return result


async def retrieve_private_service(pk: UUID, session: AsyncSession):
    repository = FlatRepository(session=session)
    result = await repository.retrieve_private(pk)
    return result


async def retrieve_flat_service(pk: UUID, session: AsyncSession):
    repository = FlatRepository(session=session)
    result = await repository.retrieve_flat(pk)
    return result


async def update_flat_service(pk: UUID, item: FlatUpdate, user: User, session: AsyncSession):
    repository = FlatRepository(session=session)
    result = await repository.update_flat(pk, item, user)
    return result


async def post_flat_service(item: FlatCreate, user: User, session: AsyncSession):
    item_dict = item.dict()
    item_dict['user_id'] = user.id
    photo_list = item_dict.pop('photos')
    flat_instance = Flat(**item_dict)
    repository = FlatRepository(session=session)
    await repository.add(flat_instance)
    dict_item = object_as_dict(flat_instance)
    if photo_list:
        list_tasks = []
        saved_photos = []
        for photo in photo_list:
            item_dict_photo = {'photo': photo, 'flat_id': flat_instance.id}
            task = asyncio.create_task(create_photo_and_s3_object(item_dict_photo))
            list_tasks.append(task)
        photos_gather = await asyncio.gather(*list_tasks)
        for photo in photos_gather:
            saved_photos.append({'id': photo.id, 'photo': photo.photo})
        dict_item['photos'] = saved_photos
    flat_serializer = FlatSchema(**dict_item)
    await send_message_about_created_flat_service(dict_item)
    return flat_serializer


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


async def send_message_about_created_flat_service(dict_item):
    message = dict_item.copy()
    message.pop('user_id')
    message.pop('count_rentings')
    message.pop('cost')
    dict_item['id'] = str(dict_item['id'])
    con = pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=5672,
        credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME,
                                          password=RABBITMQ_PASSWORD,
                                          erase_on_connect=True))
    connection = pika.BlockingConnection(con)
    channel = connection.channel()

    channel.queue_declare(queue='flat_create')
    channel.basic_publish(exchange='',
                          routing_key='flat_create',
                          body=json.dumps(message))
    connection.close()
