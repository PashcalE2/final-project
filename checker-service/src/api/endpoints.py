from fastapi import APIRouter, Depends, Path, Response, status

from src.core.services import PermissionService
from src.api.dependencies import (
    verify_admin_user_id,
    get_permission_service,
)


router = APIRouter(prefix="/api/v1/permissions")


@router.post(
    "/user/{target_user_id}/check-blocking/{group_id}", status_code=status.HTTP_200_OK
)
async def check_groups_blocking(
    permission_service: PermissionService = Depends(get_permission_service),
    admin_user_id: int = Depends(verify_admin_user_id),
    group_id: int = Path(),
    target_user_id: int = Path(),
) -> Response:
    """
    Проверка блокирования групп у пользователя
    """
    _ = await permission_service.check_groups_not_blocking(
        user_id=target_user_id,
        group_id=group_id,
    )
    return Response(status_code=status.HTTP_200_OK)
