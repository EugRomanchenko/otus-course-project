from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, List
from fastapi import UploadFile, HTTPException

from app.models import Certificate
from app.parser import parse_x509


async def save_certificate_info(
        session: AsyncSession,
        file: UploadFile
) -> Certificate:
    context = parse_x509.parse_x509_der(await file.read())
    certificate = Certificate(
        expired_at=context["expired_at"],
        created_at=context["created_at"],
        fingerprint_sha1=context["fingerprint_sha1"],
        serial_number=context["serial_number"],
        issuer=context["issuer"],
        subject=context["subject"]
    )
    certificate_match = await find_certificate_by_fingerprint(session, certificate.fingerprint_sha1)
    if certificate_match is None:
        session.add(certificate)
        await session.commit()
        return certificate
    else:
        raise HTTPException(
            status_code=409,
            detail=f"Certificate with this fingerprint: {certificate.fingerprint_sha1} already exist",
        )


async def find_certificate_by_fingerprint(
        session: AsyncSession,
        fingerprint: str,
) -> Certificate:
    stmt = select(Certificate).where(Certificate.fingerprint_sha1 == fingerprint)
    certificate = await session.scalar(stmt)
    return certificate


async def find_all_certificates(
        session: AsyncSession
) -> Sequence[Certificate]:
    stmt = select(Certificate).order_by(Certificate.id)
    certificates = (await session.scalars(stmt)).all()
    return certificates
