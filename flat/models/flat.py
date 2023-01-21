import uuid

from sqlalchemy import Column, Boolean, BigInteger, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from fastapi_users_db_sqlalchemy import GUID

from base import Base


class Flat(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True, server_default=text('uuid_generate_v4()'))
    cost = Column(BigInteger)
    user_id = Column(GUID, ForeignKey('user.id'))
    user = relationship('User')
    is_active = Column(Boolean, nullable=False, default=False, server_default='f')


flat = Flat.__table__
