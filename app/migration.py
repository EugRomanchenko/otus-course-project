from sqlalchemy.ext.asyncio import create_async_engine

from alembic import command, config
from config.settings import settings


def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


async def run_async_upgrade():
    async_engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URI,)
    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, config.Config("app/alembic.ini"))
