from typing import Annotated
from fastapi import APIRouter, UploadFile, Request, Form, File
from fastapi.templating import Jinja2Templates
from pathlib import Path
import magic

UPLOAD_DIR = Path() / 'uploads'

router = APIRouter(prefix="/upload", tags=["upload"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def upload_file_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="upload.html"
    )


@router.post("/uploadfile")
async def create_upload_file(
        file_upload: UploadFile,
):
    buffer = file_upload.file.read(1024)
    mime_type = magic.from_buffer(buffer, True)
    file_upload.file.seek(0)
    return {
        "filename": file_upload.filename,
        "content_type": mime_type,
    }

