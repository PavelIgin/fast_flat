import os
import uuid

from sqlalchemy import Column, ForeignKey, text
from sqlalchemy_utils import URLType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from fastapi_users_db_sqlalchemy import GUID


from base import Base


class Photo(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True,
                server_default=text('uuid_generate_v4()'))
    flat_id = Column(GUID, ForeignKey('flat.id'))
    flat = relationship('Flat')
    photo = Column(URLType)

photo = Photo.__table__

