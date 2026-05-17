from abc import abstractmethod

from src.core.models import PermissionSchema


class AuthService:
    @abstractmethod
    async def get_user_id(self, token: str) -> int: ...


class PermissionService:
    @abstractmethod
    async def verify_admin(
        self,
        user_id: int,
    ) -> bool: ...

    @abstractmethod
    async def get_resource_permissions(
        self,
        resource_id: int,
    ) -> list[PermissionSchema]: ...

    @abstractmethod
    async def revoke_groups(
        self,
        target_user_id: int,
        groups: list[int],
    ) -> None: ...

    @abstractmethod
    async def grant_groups(
        self,
        target_user_id: int,
        groups: list[int],
    ) -> None: ...

    @abstractmethod
    async def check_groups_blocking(
        self,
        target_user_id: int,
        groups: list[int],
    ) -> None: ...
