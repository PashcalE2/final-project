from fastapi import status, HTTPException
from aiohttp import ClientSession

from src.core.services import AuthService, PermissionService
from src.core.models import RabbitMQRequestSchema, GroupConflictScheme
from src.core.repositories import PermissionRepository
from src.settings import Settings, get_settings


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

    async def check_groups_not_blocking(
        self,
        user_id: int,
        group_id: int,
    ) -> bool:
        user_groups: list[int] = await self.repository.get_user_group_id_list(
            user_id=user_id
        )

        if group_id in user_groups:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Эта группа уже выдана"
            )

        conflict_rules_list: list[
            GroupConflictScheme
        ] = await self.repository.get_group_conflicts(group_id_list=user_groups)

        for group_conflict in conflict_rules_list:
            if group_id == group_conflict.group_id_2:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=group_conflict.reason
                )

        return True
