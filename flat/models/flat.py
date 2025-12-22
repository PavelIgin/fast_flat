import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import query_expression, relationship

from base import Base


class Flat(Base):

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True,
        server_default=text("uuid_generate_v4()"),
    )
    cost = Column(Integer)
    quadrature = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    is_active = Column(
        Boolean, nullable=False, default=False, server_default="f"
    )
    count_rentings = query_expression()
    type_promotion = query_expression()

    user = relationship("User")
    photos = relationship("Photo")
    rentings = relationship("Renting")

    __table_args__ = (
        CheckConstraint(floor >= 0, name="check_floor_positive"),
        CheckConstraint(quadrature >= 0, name="check_quadrature_positive"),
        {},
    )


# flat = Flat.__table__
