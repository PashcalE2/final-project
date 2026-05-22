from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories import PermissionRepository
from src.core.models import (
    PermissionSchema,
    GroupSchema,
    GroupConflictScheme,
)
from src.database.postgres.models import Group, Permission, UserGroup, GroupConflict
from src.settings import Settings, get_settings


settings: Settings = get_settings()


class PermissionRepositoryImpl(PermissionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_admin_group(self) -> GroupSchema:
        stmt = select(Group).where(Group.name == settings.backend.admin_group_name)
        result = await self.session.execute(stmt)
        group: Group = result.scalar_one()
        return GroupSchema(**group.as_dict())

    async def get_user_groups(
        self,
        user_id: int,
    ) -> list[GroupSchema]:
        subq = select(UserGroup.group_id).where(UserGroup.user_id == user_id)
        stmt = select(Group).where(Group.id.in_(subq))
        result = await self.session.execute(stmt)
        return list(GroupSchema(**g.as_dict()) for g in result.scalars().all())

    async def get_user_group_id_list(self, user_id: int) -> list[int]:
        subq = select(UserGroup.group_id).where(UserGroup.user_id == user_id)
        stmt = select(Group.id).where(Group.id.in_(subq))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_groups_permissions(
        self,
        group_id_list: list[int],
    ) -> list[PermissionSchema]:
        stmt = select(Permission).where(Permission.group_id.in_(group_id_list))
        result = await self.session.execute(stmt)
        return list(PermissionSchema(**p.as_dict()) for p in result.scalars().all())

    async def get_group_conflicts(
        self,
        group_id_list: list[int],
    ) -> list[GroupConflictScheme]:
        stmt = select(GroupConflict).where(GroupConflict.group_id_1.in_(group_id_list))
        result = await self.session.execute(stmt)
        return list(GroupConflictScheme(**c.as_dict()) for c in result.scalars().all())
