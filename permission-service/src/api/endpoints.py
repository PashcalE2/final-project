from fastapi import APIRouter, Depends, Path, Response, status

from src.core.services import PermissionService
from src.core.models import IdListSchema, PermissionListSchema
from src.api.dependencies import (
    verify_common_user_id,
    verify_admin_user_id,
    get_permission_service,
)


router = APIRouter(prefix="/api/v1/permissions")


@router.get("", status_code=status.HTTP_200_OK)
async def get_user_permissions(
    user_id: int = Depends(verify_common_user_id),
) -> PermissionListSchema:
    """
    Получение всех прав у данного пользователя
    """
    return None


@router.get("/resource/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource_permissions(
    permission_service: PermissionService = Depends(get_permission_service),
    user_id: int = Depends(verify_common_user_id),
    resource_id: int = Path(),
) -> PermissionListSchema:
    """
    Получение необходимого доступа для конкретного ресурса
    """
    return PermissionListSchema(
        root=await permission_service.get_resource_permissions(resource_id)
    )


@router.post("/user/{target_user_id}", status_code=status.HTTP_201_CREATED)
async def grant_groups(
    groups: IdListSchema,
    permission_service: PermissionService = Depends(get_permission_service),
    admin_user_id: int = Depends(verify_admin_user_id),
    target_user_id: int = Path(),
) -> Response:
    """
    Выдача группы прав пользователю
    """
    await permission_service.grant_groups(
        target_user_id=target_user_id,
        groups=groups.root,
    )
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/user/{target_user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_groups(
    groups: IdListSchema,
    permission_service: PermissionService = Depends(get_permission_service),
    admin_user_id: int = Depends(verify_admin_user_id),
    target_user_id: int = Path(),
) -> Response:
    """
    Отзыв групп прав у пользователя
    """
    await permission_service.revoke_groups(
        target_user_id=target_user_id,
        groups=groups.root,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/user/{target_user_id}", status_code=status.HTTP_200_OK)
async def check_groups_blocking(
    groups: IdListSchema,
    permission_service: PermissionService = Depends(get_permission_service),
    admin_user_id: int = Depends(verify_admin_user_id),
    target_user_id: int = Path(),
) -> Response:
    """
    Проверка блокирования групп у пользователя
    """
    await permission_service.revoke_groups(
        target_user_id=target_user_id,
        groups=groups.root,
    )
    return Response(status_code=status.HTTP_200_OK)
