from fastapi import status, HTTPException
from faststream import Depends
from faststream.rabbit import RabbitBroker

from src.core.models import (
    CheckGroupBlockingRequestSchema,
    CheckGroupBlockingResponseSchema,
)
from src.core.services import PermissionService
from src.api.dependencies import get_permission_service
from src.settings import settings


broker = RabbitBroker(url=str(settings.rabbitmq.dsn))


@broker.subscriber("check-groups-blocking-request")
@broker.publisher("check-groups-blocking-response")
async def check_groups_blocking(
    data: CheckGroupBlockingRequestSchema,
    permission_service: PermissionService = Depends(get_permission_service),
) -> str:
    try:
        await permission_service.check_groups_blocking(
            target_user_id=data.target_user_id,
            groups=data.groups,
        )
        return CheckGroupBlockingResponseSchema(
            request_id=data.request_id,
            status=status.HTTP_200_OK,
            detail=None,
        ).model_dump_json()
    except HTTPException as e:
        return CheckGroupBlockingResponseSchema(
            request_id=data.request_id,
            status=e.status_code,
            detail=e.detail,
        ).model_dump_json()
    except Exception as e:
        return CheckGroupBlockingResponseSchema(
            request_id=data.request_id,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ).model_dump_json()
