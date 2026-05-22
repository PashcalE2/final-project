from pydantic import BaseModel, RootModel


class PermissionSchema(BaseModel):
    id: int
    group_id: int
    name: str


class GroupSchema(BaseModel):
    id: int
    name: str
    description: str | None


class RabbitMQRequestSchema(BaseModel):
    request_id: int
    user_id: int
    group_id: int


class RabbitMQResponseSchema(BaseModel):
    request_id: int
    status: int
    detail: str | None


class GroupConflictScheme(BaseModel):
    group_id_1: int
    group_id_2: int
    reason: str
