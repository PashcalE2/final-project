import abc
from typing import Protocol

from src.core.models import LoginSchema, UserModelSchema


class AuthRepository(Protocol):
    @abc.abstractmethod
    async def add(self, data: LoginSchema) -> UserModelSchema: ...

    @abc.abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserModelSchema: ...

    @abc.abstractmethod
    async def get_user_by_login(self, login: str) -> UserModelSchema: ...
