from abc import abstractmethod

from src.core.models import (
    PermissionSchema,
    PermissionListSchema,
    GroupSchema,
    RequestSchema,
)


class PermissionRepository:
    @abstractmethod
    async def get_admin_group(self) -> GroupSchema: ...

    @abstractmethod
    async def get_user_permissions(self, user_id: int) -> PermissionListSchema: ...

    @abstractmethod
    async def get_resource_permission(self, resource_id: int) -> PermissionSchema: ...

    @abstractmethod
    async def get_user_groups(self, user_id: int) -> list[GroupSchema]: ...

    @abstractmethod
    async def delete_user_groups(
        self,
        user_id: int,
        group_id_list: list[GroupSchema],
    ) -> None: ...

    @abstractmethod
    async def add_user_groups(
        self,
        user_id: int,
        group_id_list: list[GroupSchema],
    ) -> None: ...

    @abstractmethod
    async def add_new_request(self, user_id: int, group_id: int) -> RequestSchema: ...

    @abstractmethod
    async def update_request(
        self,
        request_id: int,
        description: str | None,
    ) -> None: ...
