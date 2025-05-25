import uuid

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from base import Base
from flat.enums import PromotionEnum


class Promotion(Base):
    """
    Model defines what in order be flat in user list
    """

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True,
        server_default=text("uuid_generate_v4()"),
    )
    type = Column(Integer)
    start = Column(DateTime, doc="date start promotion ")
    end = Column(DateTime, doc="date stop promotion")

    flat_id = Column(UUID(as_uuid=True), ForeignKey("flat.id"))
    flat = relationship("Flat")

    __table_args__ = (
        CheckConstraint(
            type <= PromotionEnum.get_count_elements(), name="check_type_max"
        ),
        CheckConstraint(type > 0, name="check_type_positive"),
    )
