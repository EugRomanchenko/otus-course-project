from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config.settings import settings


async_engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
    #url="postgresql+asyncpg://postgres:changethis@localhost/app",
    echo_pool=True,
)
session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)


async def session_dependency():
    async with session_factory() as session:
        yield session
