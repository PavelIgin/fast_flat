import uuid

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import (  # Date,
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    SmallInteger,
    text,
)
from sqlalchemy.dialects.postgresql import DATERANGE, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from base import Base


class Renting(Base):

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    lease_range = Column(DATERANGE, nullable=False)
    # start = Column(Date, nullable=False) # todo переделать на 2 отдельных поля т.к с выдачей таких данных тяжеловато,
    # end = Column(Date, nullable=False)
    cost = Column(BigInteger)
    count_guest = Column(SmallInteger)

    user_id = Column(GUID, ForeignKey("user.id"))
    flat_id = Column(UUID(as_uuid=True), ForeignKey("flat.id"))

    user = relationship("User")
    flat = relationship("Flat", back_populates="rentings")

    status = Column(
        Boolean, default=False, server_default=expression.null(), nullable=True
    )

    @property
    def date_range(cls):
        return cls.lease_range.upper, cls.lease_range.lower
