from typing import AsyncGenerator
from redis.asyncio import Redis, ConnectionPool

from src.settings import Settings, get_settings


settings: Settings = get_settings()
pool = ConnectionPool.from_url(
    str(settings.redis.dsn),
    max_connections=settings.redis.max_connections,
    decode_responses=settings.redis.decode_responses,
)


async def get_redis_session() -> AsyncGenerator[Redis]:
    redis_client = Redis(connection_pool=pool)
    yield redis_client
    await redis_client.aclose()
