import logging

from fastapi import APIRouter, UploadFile, Request, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

from crud import save_certificate_info
from db.engine import session_dependency
from config.settings import settings


router = APIRouter(prefix="/upload", tags=["upload"])
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def upload_file_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="upload.html"
    )


@router.post("/")
async def create_upload_file(
        file_upload: UploadFile,
        async_session: AsyncSession = Depends(session_dependency),
):
    if Path(file_upload.filename).suffix not in settings.ALLOWED_FILE_TYPE_EXT:
        raise HTTPException(
            status_code=415,
            detail="File type not allowed"
        )
    cert = await save_certificate_info(session=async_session, file=file_upload)
    return RedirectResponse(
        f"http://127.0.0.1:8000/view/{cert.fingerprint_sha1}/",
        status_code=status.HTTP_303_SEE_OTHER
    )

