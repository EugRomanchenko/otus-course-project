from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CertificateBase(BaseModel):
    expired_at: datetime
    created_at: datetime
    fingerprint_sha1: str
    serial_number: int
    issuer: str
    subject: str


class Certificate(CertificateBase):
    uploaded_at: datetime
    id: int

    model_config = ConfigDict(from_attributes=True)
