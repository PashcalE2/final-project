from fastapi import status, HTTPException
from aiohttp import ClientSession

from src.settings import settings
from src.core.services import AuthService, PermissionService
from src.core.models import PermissionSchema


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
    async def verify_admin(
        self,
        user_id: int,
    ) -> bool:
        pass

    async def get_resource_permissions(
        self,
        resource_id: int,
    ) -> list[PermissionSchema]:
        pass

    async def revoke_groups(
        self,
        target_user_id: int,
        groups: list[int],
    ) -> None:
        pass

    async def grant_groups(
        self,
        target_user_id: int,
        groups: list[int],
    ) -> None:
        pass

    async def check_groups_blocking(
        self,
        target_user_id: int,
        groups: list[int],
    ) -> None:
        pass
