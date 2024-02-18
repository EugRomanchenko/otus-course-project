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
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )

    expired_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    fingerprint_sha1 = Column(
        String,
        unique=True,
        nullable=False,
    )

    serial_number = Column(
        Integer,
        unique=False,
        nullable=True,
    )

    issuer = Column(
        String,
        unique=False,
        nullable=True,
    )

    subject = Column(
        String,
        unique=False,
        nullable=True,
    )

    #def __str__(self):
    #    return (
    #        f"(fingerprint={self.fingerprint_sha1}, expired={self.expired_at})"
    #    )
        #return {
        #    "expired_at": self.expired_at,
        #    "created_at": self.created_at,
        #    "uploaded_at": self.uploaded_at,
        #    "fingerprint_sha1": self.fingerprint_sha1,
        #    "serial_number": self.serial_number,
        #    "issuer": self.issuer,
        #    "subject": self.subject,
        #}

    #def __repr__(self):
    #    return str(self)
