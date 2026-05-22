from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from faststream import Depends as DependsFS

from src.core.services import AuthService, PermissionService
from src.core.repositories import PermissionRepository
from src.impl.services import AuthServiceImpl, PermissionServiceImpl
from src.impl.repositories import PermissionRepositoryImpl
from src.database.postgres.session import get_postgres_session


async def get_aiohttp_session() -> AsyncGenerator[ClientSession]:
    async with ClientSession() as session:
        yield session


async def get_auth_service(
    session: ClientSession = Depends(get_aiohttp_session),
) -> AuthService:
    return AuthServiceImpl(session=session)


bearer_schema = HTTPBearer()


async def get_permission_repository(
    session: AsyncSession = Depends(get_postgres_session),
) -> PermissionRepository:
    return PermissionRepositoryImpl(session=session)


async def get_permission_service(
    permission_repository: PermissionRepository = Depends(get_permission_repository),
) -> PermissionService:
    return PermissionServiceImpl(
        repository=permission_repository,
        admin_group_id=(await permission_repository.get_admin_group()).id,
    )


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


async def get_permission_repository_faststream(
    session: AsyncSession = DependsFS(get_postgres_session),
) -> PermissionRepository:
    return PermissionRepositoryImpl(session=session)


async def get_permission_service_faststream(
    permission_repository: PermissionRepository = DependsFS(
        get_permission_repository_faststream
    ),
) -> PermissionService:
    return PermissionServiceImpl(
        repository=permission_repository,
        admin_group_id=(await permission_repository.get_admin_group()).id,
    )
