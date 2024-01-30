from datetime import datetime
from pydantic import BaseModel


class CertificateBase(BaseModel):
    expired_at: datetime
    created_at: datetime
    fingerprint_sha1: str


class Certificate(CertificateBase):
    uploaded_at: datetime
    id: int

    class Config:
        orm_mode = True
