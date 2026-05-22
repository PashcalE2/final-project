from abc import abstractmethod


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
    async def check_groups_not_blocking(
        self,
        user_id: int,
        group_id: int,
    ) -> bool: ...
