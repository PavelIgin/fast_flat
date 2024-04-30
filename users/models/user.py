from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String

from base import Base


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = "user"

    username = Column(String)
    telegram_contact = Column(String)
