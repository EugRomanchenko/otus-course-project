from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.settings import settings


async_engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
    echo_pool=False,
    echo=False,
)
session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)


async def session_dependency():
    async with session_factory() as session:
        yield session
