from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Sequence
from fastapi import UploadFile, HTTPException
from datetime import timedelta, datetime

from models import Certificate
from parser import parse_x509


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


async def find_expired_certificates(
        session: AsyncSession,
        time_delta: timedelta,
) -> Sequence[Certificate]:
    current_time = datetime.utcnow()
    expired_time = current_time + time_delta
    stmt = select(Certificate).where(Certificate.expired_at <= expired_time)
    certificates = (await session.scalars(stmt)).all()
    return certificates


async def delete_expired_certificates(
        session: AsyncSession,
        time_delta: timedelta,
):
    current_time = datetime.utcnow()
    expired_time = current_time + time_delta
    stmt = delete(Certificate).where(Certificate.expired_at <= expired_time)
    await session.execute(stmt)
    await session.commit()


async def delete_certificate_by_fingerprint(
        session: AsyncSession,
        fingerprint: str,
):
    certificate = await find_certificate_by_fingerprint(session, fingerprint)
    if certificate is None:
        raise HTTPException(
            status_code=404,
            detail=f"Certificate with this fingerprint: {fingerprint} can't be deleted because it not exist",
        )
    await session.delete(certificate)
    await session.commit()
