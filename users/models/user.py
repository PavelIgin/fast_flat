import uuid

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, GUID
from sqlalchemy import Column, String, Boolean

from base import Base


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = "user"

    username = Column(String)
    telegram_contact = Column(String)
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)