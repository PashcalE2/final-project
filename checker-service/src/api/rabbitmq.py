from fastapi import status, HTTPException
from faststream import Depends, FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from src.core.models import (
    RabbitMQRequestSchema,
    RabbitMQResponseSchema,
)
from src.core.services import PermissionService
from src.api.dependencies import get_permission_service_faststream
from src.settings import Settings, get_settings


settings: Settings = get_settings()
broker = RabbitBroker(url=str(settings.rabbitmq.dsn))
app = FastStream(broker)

request_queue = RabbitQueue("request", durable=True)
response_queue = RabbitQueue("response", durable=True)


@broker.subscriber(queue=request_queue)
async def check_groups_blocking(
    json: str,
    permission_service: PermissionService = Depends(get_permission_service_faststream),
) -> None:
    data: RabbitMQRequestSchema = RabbitMQRequestSchema.model_validate_json(json)
    result: RabbitMQResponseSchema
    try:
        await permission_service.check_groups_not_blocking(
            user_id=data.user_id,
            group_id=data.group_id,
        )
        result = RabbitMQResponseSchema(
            request_id=data.request_id,
            status=status.HTTP_200_OK,
            detail=None,
        )
    except HTTPException as e:
        result = RabbitMQResponseSchema(
            request_id=data.request_id,
            status=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        result = RabbitMQResponseSchema(
            request_id=data.request_id,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    await broker.publish(
        result.model_dump_json(),
        queue=response_queue,
    )
