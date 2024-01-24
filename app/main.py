from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import upload

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(upload.router)


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def base_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="base.html"
    )
