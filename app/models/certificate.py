from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func

from models.base import Base


class Certificate(Base):

    uploaded_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow(),
        server_default=func.now,
    )

    expired_at = Column(
        DateTime,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        nullable=False,
    )

    fingerprint_sha1 = Column(
        String,
        unique=True,
        nullable=False
    )
