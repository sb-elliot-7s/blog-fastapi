from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from settings_config import get_settings

_settings = get_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{_settings.postgres_user}:" \
                          f"{_settings.postgres_password}@" \
                          f"{_settings.postgres_server}:" \
                          f"{_settings.postgres_port}/{_settings.postgres_db_name}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
