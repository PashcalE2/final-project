import abc
from typing import Protocol

from src.core.models import (
    LoginSchema,
    TokensPairSchema,
    AccessTokenSchema,
)


class AuthService(Protocol):
    @abc.abstractmethod
    async def register(self, data: LoginSchema) -> TokensPairSchema: ...

    @abc.abstractmethod
    async def login(self, data: LoginSchema) -> TokensPairSchema: ...

    @abc.abstractmethod
    async def get_new_access_token(self, refresh_token: str) -> AccessTokenSchema: ...
