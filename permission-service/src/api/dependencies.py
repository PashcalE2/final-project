from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from aiohttp import ClientSession

from src.core.services import AuthService, PermissionService
from src.impl.services import AuthServiceImpl, PermissionServiceImpl


async def get_aiohttp_session() -> AsyncGenerator[ClientSession]:
    async with ClientSession() as session:
        yield session


async def get_auth_service(
    session: ClientSession = Depends(get_aiohttp_session),
) -> AuthService:
    return AuthServiceImpl(session=session)


bearer_schema = HTTPBearer()


async def verify_common_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: HTTPAuthorizationCredentials = Depends(bearer_schema),
) -> int:
    return await auth_service.get_user_id(token=token.credentials)


async def get_permission_service() -> PermissionService:
    return PermissionServiceImpl()


async def verify_admin_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    permission_service: PermissionService = Depends(get_permission_service),
    token: HTTPAuthorizationCredentials = Depends(bearer_schema),
) -> int:
    user_id: int = await auth_service.get_user_id(token=token.credentials)
    is_admin: bool = await permission_service.verify_admin(user_id=user_id)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not admin"
        )
    return user_id
