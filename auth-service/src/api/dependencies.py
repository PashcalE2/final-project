from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.impl.repository import AuthRepositoryImpl
from src.impl.service import AuthServiceImpl
from src.database.postgres.session import get_postgres_session
from src.database.redis.session import get_redis_session
from src.core.models import UserModelSchema
from src.core.repository import AuthRepository
from src.core.service import AuthService
from src.security.jwt import decode_access_token


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
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Broken token",
        )

    expires: str = data.get("expires")
    if expires is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Broken token",
        )

    if datetime.now().timestamp() > int(expires):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired",
        )

    user_id: str = data.get("id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Broken token",
        )

    user_id: int = int(user_id)
    user: UserModelSchema = await auth_repository.get_user_by_id(user_id)
    return user
