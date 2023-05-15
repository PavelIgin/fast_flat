import uuid

from sqlalchemy import Column, BigInteger, ForeignKey, SmallInteger, text, Boolean
from sqlalchemy.dialects.postgresql import UUID, DATERANGE
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from fastapi_users_db_sqlalchemy import GUID

from base import Base


class Renting(Base):

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True,
                default=uuid.uuid4, server_default=text('uuid_generate_v4()'))
    lease_range = Column(DATERANGE(), nullable=False)
    cost = Column(BigInteger)
    count_guest = Column(SmallInteger)

    user_id = Column(GUID, ForeignKey('user.id'))
    flat_id = Column(UUID(as_uuid=True), ForeignKey('flat.id'))

    user = relationship('User')
    flat = relationship('Flat')

    status = Column(Boolean, default=False, server_default=expression.null(), nullable=True)

    @property
    def date_range(cls):
        return cls.lease_range.upper, cls.lease_range.lower
