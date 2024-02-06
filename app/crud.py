from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
        fingerprint_sha1=context["fingerpint_sha1"],
    )
    certificate_match = await find_certificate_by_fingerprint(session, certificate.fingerprint_sha1)
    if certificate.fingerprint_sha1 == certificate_match.fingerprint_sha1:
        raise HTTPException(
            status_code=409,
            detail=f"Certificate with this fingerprint: {certificate.fingerprint_sha1} already exist",
        )
    session.add(certificate)
    await session.commit()
    return certificate


async def find_certificate_by_fingerprint(
        session: AsyncSession,
        fingerprint: str,
) -> Certificate:
    stmt = select(Certificate).where(Certificate.fingerprint_sha1 == fingerprint)
    certificate = await session.scalar(stmt)
    return certificate
