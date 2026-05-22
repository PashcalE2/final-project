from abc import abstractmethod
from faststream.rabbit import RabbitBroker, RabbitQueue

from src.core.models import (
    PermissionListSchema,
    PermissionSchema,
    RabbitMQResponseSchema,
)


class AuthService:
    @abstractmethod
    async def get_user_id(self, token: str) -> int: ...


class PermissionService:
    @abstractmethod
    async def get_user_permissions(self, user_id: int) -> PermissionListSchema: ...

    @abstractmethod
    async def verify_admin(
        self,
        user_id: int,
    ) -> bool: ...

    @abstractmethod
    async def get_resource_permission(
        self,
        resource_id: int,
    ) -> PermissionSchema: ...

    @abstractmethod
    async def revoke_groups(
        self,
        target_user_id: int,
        group_id_list: list[int],
    ) -> None: ...

    @abstractmethod
    async def grant_groups(
        self,
        target_user_id: int,
        group_id_list: list[int],
    ) -> None: ...

    @abstractmethod
    async def check_groups_not_blocking(
        self,
        broker: RabbitBroker,
        queue: RabbitQueue,
        user_id: int,
        group_id: int,
    ) -> None: ...

    @abstractmethod
    async def save_check_result(
        self,
        response: RabbitMQResponseSchema,
    ) -> None: ...
