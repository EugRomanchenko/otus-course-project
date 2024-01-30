from fastapi import APIRouter, UploadFile, Request
from fastapi.templating import Jinja2Templates
import magic

from app.parser import parse_x509


router = APIRouter(prefix="/upload", tags=["upload"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def upload_file_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="upload.html"
    )


@router.post("/")
async def create_upload_file(
        file_upload: UploadFile,
):
    contents = await file_upload.read()
    information = parse_x509.parse_x509_der(contents)
    print(information)
    return information

