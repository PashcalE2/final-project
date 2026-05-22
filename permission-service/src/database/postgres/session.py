from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from src.settings import Settings, get_settings


settings: Settings = get_settings()
sqlalchemy_database_url = str(settings.db.dsn)
async_engine = create_async_engine(sqlalchemy_database_url, pool_pre_ping=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            yield session
