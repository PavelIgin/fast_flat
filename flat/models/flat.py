import uuid

from sqlalchemy import Column, String, Integer, Boolean, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from fastapi_users_db_sqlalchemy import GUID

from base import Base


class Flat(Base):

    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True, unique=True)
    cost = Column(BigInteger)
    user = Column(GUID, ForeignKey('user.id'))
    user_id = relationship('User')
    is_active = Column(Boolean)
