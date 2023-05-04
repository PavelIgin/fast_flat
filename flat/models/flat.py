import uuid

from sqlalchemy import Column, Boolean, Integer, ForeignKey, text, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from fastapi_users_db_sqlalchemy import GUID

from base import Base


class Flat(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True,
                server_default=text('uuid_generate_v4()'))
    cost = Column(Integer)
    quadrature = Column(Integer, )
    floor = Column(Integer, )
    address = Column(String, )
    user_id = Column(GUID, ForeignKey('user.id'))
    is_active = Column(Boolean, nullable=False, default=False, server_default='f')

    user = relationship('User')
    photos = relationship('Photo')

    __table_args__ = (
        CheckConstraint(floor >= 0, name='check_bar_positive'),
        CheckConstraint(quadrature >= 0, name='check_bar_positive'),
        {})


flat = Flat.__table__
