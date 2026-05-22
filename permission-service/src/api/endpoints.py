from fastapi import APIRouter, Depends, Path, Response, status
from faststream import Depends as DependsFS

from src.core.services import PermissionService
from src.core.models import (
    IdListSchema,
    PermissionListSchema,
    PermissionSchema,
    RabbitMQResponseSchema,
)
from src.api.dependencies import (
    verify_common_user_id,
    verify_admin_user_id,
    get_permission_service,
    get_permission_service_faststream,
)
from src.api.rabbitmq import broker, request_queue, response_queue


router = APIRouter(prefix="/api/v1/permissions")


@router.get("", status_code=status.HTTP_200_OK)
async def get_user_permissions(
    permission_service: PermissionService = Depends(get_permission_service),
    user_id: int = Depends(verify_common_user_id),
) -> PermissionListSchema:
    """
    Получение всех прав у данного пользователя
    """
    return await permission_service.get_user_permissions(user_id=user_id)


@router.get("/resource/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource_permission(
    permission_service: PermissionService = Depends(get_permission_service),
    user_id: int = Depends(verify_common_user_id),
    resource_id: int = Path(),
) -> PermissionSchema:
    """
    Получение необходимого доступа для конкретного ресурса
    """
    return await permission_service.get_resource_permission(resource_id)


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
        group_id_list=groups.root,
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
        group_id_list=groups.root,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/request/{group_id}", status_code=status.HTTP_201_CREATED)
async def request_group(
    group_id: int = Path(),
    permission_service: PermissionService = Depends(get_permission_service),
    user_id: int = Depends(verify_common_user_id),
):
    await permission_service.check_groups_not_blocking(
        broker=broker,
        queue=request_queue,
        user_id=user_id,
        group_id=group_id,
    )
    return Response(status_code=status.HTTP_201_CREATED)


@broker.subscriber(queue=response_queue)
async def save_check_result(
    json: str,
    permission_service: PermissionService = DependsFS(
        get_permission_service_faststream
    ),
) -> None:
    data: RabbitMQResponseSchema = RabbitMQResponseSchema.model_validate_json(json)
    print(f"{'=' * 20}\n SKIBIDI \n {'=' * 20}")
    await permission_service.save_check_result(response=data)
