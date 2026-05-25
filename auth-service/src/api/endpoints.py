from fastapi.routing import APIRouter
from fastapi import Query, Depends

from src.core.models import (
    LoginSchema,
    TokensPairSchema,
    AccessTokenSchema,
    UserIdSchema,
    RefreshTokenSchema,
    UserModelSchema,
)
from src.core.service import AuthService
from src.api.dependencies import get_auth_service, get_current_user


router = APIRouter(prefix="/api/v1/auth")


@router.get("/register")
async def register(
    data: LoginSchema = Query(),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokensPairSchema:
    return await auth_service.register(data=data)


@router.get("/login")
async def login(
    data: LoginSchema = Query(),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokensPairSchema:
    return await auth_service.login(data=data)


@router.get("/id")
async def get_id_from_access_token(
    user: UserModelSchema = Depends(get_current_user),
) -> UserIdSchema:
    return UserIdSchema(id=user.id)


@router.get("/refresh")
async def get_new_access_token(
    data: RefreshTokenSchema = Query(),
    auth_service: AuthService = Depends(get_auth_service),
) -> AccessTokenSchema:
    return await auth_service.get_new_access_token(data.refresh_token)
