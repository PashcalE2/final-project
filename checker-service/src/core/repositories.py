from abc import abstractmethod

from src.core.models import GroupSchema, PermissionSchema, GroupConflictScheme


class PermissionRepository:
    @abstractmethod
    async def get_admin_group(self) -> GroupSchema: ...

    @abstractmethod
    async def get_user_groups(self, user_id: int) -> list[GroupSchema]: ...

    @abstractmethod
    async def get_user_group_id_list(self, user_id: int) -> list[int]: ...

    @abstractmethod
    async def get_groups_permissions(
        self,
        group_id_list: list[int],
    ) -> list[PermissionSchema]: ...

    @abstractmethod
    async def get_group_conflicts(
        self,
        group_id_list: list[int],
    ) -> list[GroupConflictScheme]: ...
