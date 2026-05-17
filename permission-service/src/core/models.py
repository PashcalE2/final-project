from pydantic import BaseModel, RootModel


class PermissionSchema(BaseModel):
    id: int
    group_id: int
    name: str


class PermissionListSchema(RootModel):
    root: list[PermissionSchema]


class IdListSchema(RootModel):
    root: list[int]


class CheckGroupBlockingRequestSchema(BaseModel):
    request_id: int
    target_user_id: int
    groups: list[int]


class CheckGroupBlockingResponseSchema(BaseModel):
    request_id: int
    status: int
    detail: str | None
