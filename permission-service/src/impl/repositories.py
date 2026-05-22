from sqlalchemy import select, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories import PermissionRepository
from src.core.models import (
    PermissionSchema,
    PermissionListSchema,
    GroupSchema,
    RequestSchema,
)
from src.database.postgres.models import Group, Resource, Permission, UserGroup, Request
from src.settings import Settings, get_settings


settings: Settings = get_settings()


class PermissionRepositoryImpl(PermissionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.created_status_id = 1

    async def get_admin_group(self) -> GroupSchema:
        stmt = select(Group).where(Group.name == settings.backend.admin_group_name)
        result = await self.session.execute(stmt)
        group: Group = result.scalar_one()
        return GroupSchema(**group.as_dict())

    async def get_user_permissions(self, user_id: int) -> PermissionListSchema:
        stmt = (
            select(Permission)
            .join(Group, Permission.group_id == Group.id)
            .join(UserGroup, Group.id == UserGroup.group_id)
            .where(UserGroup.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        permissions: list[Permission] = list(result.scalars().all())
        return PermissionListSchema(root=permissions)

    async def get_resource_permission(
        self,
        resource_id: int,
    ) -> PermissionSchema:
        subq = select(Resource.permission_id).where(Resource.id == resource_id)
        stmt = select(Permission).where(Permission.id.in_(subq))
        result = await self.session.execute(stmt)
        permission: Permission = result.scalar_one()
        return PermissionSchema(**permission.as_dict())

    async def get_user_groups(
        self,
        user_id: int,
    ) -> list[GroupSchema]:
        subq = select(UserGroup.group_id).where(UserGroup.user_id == user_id)
        stmt = select(Group).where(Group.id.in_(subq))
        result = await self.session.execute(stmt)
        groups: list[Group] = list(result.scalars().all())
        return groups

    async def delete_user_groups(
        self,
        user_id: int,
        group_id_list: list[int],
    ) -> None:
        stmt = delete(UserGroup).where(
            (UserGroup.user_id == user_id) & (UserGroup.group_id.in_(group_id_list))
        )
        await self.session.execute(stmt)

    async def add_user_groups(
        self,
        user_id: int,
        group_id_list: list[int],
    ) -> None:
        stmt = insert(UserGroup).values(
            [
                UserGroup(user_id=user_id, group_id=group_id).as_dict()
                for group_id in group_id_list
            ]
        )
        await self.session.execute(stmt)

    async def add_new_request(self, user_id: int, group_id: int) -> RequestSchema:
        request = Request(
            user_id=user_id,
            group_id=group_id,
            status_id=self.created_status_id,
        )
        self.session.add(request)
        await self.session.commit()
        return RequestSchema(**request.as_dict())

    async def update_request(self, request_id: str, description: str | None) -> None:
        stmt = (
            update(Request)
            .where(Request.id == request_id)
            .values(description=description)
        )

        await self.session.execute(stmt)
