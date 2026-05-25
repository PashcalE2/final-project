from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.impl.repository import AuthRepositoryImpl
from src.impl.service import AuthServiceImpl
from src.database.postgres.session import get_postgres_session
from src.database.redis.session import get_redis_session
from src.core.models import UserModelSchema
from src.core.repository import AuthRepository
from src.core.service import AuthService
from src.security.jwt import decode_access_token
from src.exception import BrokenToken, UserNotFound


async def get_auth_repository(
    session: AsyncSession = Depends(get_postgres_session),
    redis: Redis = Depends(get_redis_session),
) -> AuthRepository:
    return AuthRepositoryImpl(session=session, redis=redis)


async def get_auth_service(
    repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthServiceImpl(repository=repository)


bearer_schema = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_schema),
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> UserModelSchema:
    data: dict = decode_access_token(token=token.credentials)

    user_id: int = int(data.get("id"))
    try:
        user: UserModelSchema = await auth_repository.get_user_by_id(user_id)
    except UserNotFound:
        raise BrokenToken()

    return user
