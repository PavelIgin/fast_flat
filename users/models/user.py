from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from base import Base
from sqlalchemy import Column, String


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = 'user'

    username = Column(String)
    telegram_contact = Column(String)