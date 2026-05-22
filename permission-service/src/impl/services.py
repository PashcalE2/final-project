from fastapi import status, HTTPException
from aiohttp import ClientSession
from sqlalchemy.exc import NoResultFound
from faststream.rabbit import RabbitBroker, RabbitQueue

from src.settings import Settings, get_settings
from src.core.services import AuthService, PermissionService
from src.core.models import (
    PermissionSchema,
    PermissionListSchema,
    RequestSchema,
    RabbitMQRequestSchema,
    RabbitMQResponseSchema,
)
from src.core.repositories import PermissionRepository


settings: Settings = get_settings()


class AuthServiceImpl(AuthService):
    def __init__(self, session: ClientSession):
        self.session = session

    async def get_user_id(self, token: str) -> int:
        async with self.session.get(
            f"{settings.auth_service.get_id_url}",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            result: dict = await response.json()

            if response.status != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status, detail=result.get("detail")
                )

            return int(result.get("id"))


class PermissionServiceImpl(PermissionService):
    def __init__(self, repository: PermissionRepository, admin_group_id: int):
        self.repository = repository
        self.admin_group_id = admin_group_id

    async def get_user_permissions(self, user_id: int) -> PermissionListSchema:
        return await self.repository.get_user_permissions(user_id=user_id)

    async def verify_admin(
        self,
        user_id: int,
    ) -> bool:
        groups = await self.repository.get_user_groups(user_id=user_id)
        if self.admin_group_id not in (g.id for g in groups):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not an admin",
            )
        return True

    async def get_resource_permission(
        self,
        resource_id: int,
    ) -> PermissionSchema:
        try:
            return await self.repository.get_resource_permission(
                resource_id=resource_id
            )
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found permission"
            )

    async def revoke_groups(
        self,
        target_user_id: int,
        group_id_list: list[int],
    ) -> None:
        user_groups = await self.repository.get_user_groups(user_id=target_user_id)
        user_groups = (g.id for g in user_groups)
        if not set(group_id_list).issubset(set(user_groups)):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Groups must be subset of current user groups",
            )

        await self.repository.delete_user_groups(
            user_id=target_user_id,
            group_id_list=group_id_list,
        )

    async def grant_groups(
        self,
        target_user_id: int,
        group_id_list: list[int],
    ) -> None:
        _ = await self.check_groups_not_blocking(
            user_id=target_user_id,
            group_id=group_id_list,
        )

        await self.repository.add_user_groups(
            user_id=target_user_id,
            group_id_list=group_id_list,
        )

    async def check_groups_not_blocking(
        self,
        broker: RabbitBroker,
        queue: RabbitQueue,
        user_id: int,
        group_id: int,
    ) -> None:
        request: RequestSchema = await self.repository.add_new_request(
            user_id=user_id,
            group_id=group_id,
        )
        data = RabbitMQRequestSchema(
            request_id=request.id,
            user_id=user_id,
            group_id=group_id,
        )
        await broker.publish(
            message=data.model_dump_json(),
            queue=queue,
        )

    async def save_check_result(self, response: RabbitMQResponseSchema) -> None:
        await self.repository.update_request(
            request_id=response.request_id,
            description=response.detail,
        )
