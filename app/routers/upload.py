from fastapi import APIRouter, UploadFile, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from app.crud import save_certificate_info
from app.schemas import certificate
from app.db.engine import session_dependency


router = APIRouter(prefix="/upload", tags=["upload"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def upload_file_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="upload.html"
    )


@router.post("/", response_model=certificate.Certificate)
async def create_upload_file(
        file_upload: UploadFile,
        async_session: AsyncSession = Depends(session_dependency),
):
    cert = await save_certificate_info(session=async_session, file=file_upload)
    return cert

