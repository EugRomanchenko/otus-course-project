from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from app.crud import find_certificate_by_fingerprint, find_all_certificates
from app.schemas import certificate
from app.db.engine import session_dependency


router = APIRouter(prefix="/view", tags=["view"])

templates = Jinja2Templates(directory="templates")


@router.get("/all", response_model=certificate.Certificate)
async def get_all_certificates(
        request: Request,
        async_session: AsyncSession = Depends(session_dependency),
):
    certs = await find_all_certificates(session=async_session)
    return templates.TemplateResponse(
        "view_all.html",
        {
            "request": request,
            "certs": certs
        }
    )


@router.get("/{fingerprint_id}")
async def get_certificate_by_fingerprint_id(
        request: Request,
        fingerprint_id: str,
        async_session: AsyncSession = Depends(session_dependency),
):
    cert = await find_certificate_by_fingerprint(session=async_session, fingerprint=fingerprint_id)
    if cert is None:
        raise HTTPException(
            status_code=404,
            detail="Page not found"
        )
    return templates.TemplateResponse(
        request=request,
        name="view.html",
        context={
            "expired_at": cert.expired_at,
            "created_at": cert.created_at,
            "uploaded_at": cert.uploaded_at,
            "fingerprint_sha1": cert.fingerprint_sha1,
            "serial_number": cert.serial_number,
            "issuer": cert.issuer,
            "subject": cert.subject,
        }
    )
