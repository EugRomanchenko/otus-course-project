import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from routers import upload, view, delete
from migration import run_async_upgrade
from scheduler import middleware


logging.getLogger(__name__).setLevel(logging.INFO)
logger = logging


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Starting up...")
    logger.info("run alembic upgrade head...")
    await run_async_upgrade()
    yield
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan, middleware=middleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(upload.router)
app.include_router(view.router)
app.include_router(delete.router)


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def base_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="base.html"
    )
