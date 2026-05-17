from sqlalchemy.exc import NoResultFound

from src.core.repository import AuthRepository
from src.core.service import AuthService
from src.core.models import (
    AccessTokenSchema,
    LoginSchema,
    TokensPairSchema,
    UserModelSchema,
)
from src.security.password import verify_password, get_password_hash
from src.security.jwt import (
    create_refresh_token,
    create_access_token,
    decode_refresh_token,
)


class AuthServiceImpl(AuthService):
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    async def register(self, data: LoginSchema) -> TokensPairSchema:
        user: UserModelSchema | None = None

        try:
            user = await self.repository.get_user_by_login(
                login=data.login,
            )
        except NoResultFound:
            pass

        if user is not None:
            raise

        data.password = get_password_hash(data.password)
        user: UserModelSchema = await self.repository.add(data)

        return TokensPairSchema(
            refresh_token=create_refresh_token(user),
            access_token=create_access_token(user),
        )

    async def login(self, data: LoginSchema) -> TokensPairSchema:
        user: UserModelSchema = await self.repository.get_user_by_login(data.login)

        if not verify_password(
            plain_password=data.password,
            hashed_password=user.password,
        ):
            raise

        return TokensPairSchema(
            refresh_token=create_refresh_token(user),
            access_token=create_access_token(user),
        )

    async def get_new_access_token(self, refresh_token: str) -> AccessTokenSchema:
        data = decode_refresh_token(token=refresh_token)
        if data is None:
            raise

        user_id: str | None = data["id"]
        if user_id is None:
            raise

        user_id: int = int(user_id)
        user: UserModelSchema = await self.repository.get_user_by_id(user_id)

        return TokensPairSchema(
            refresh_token=create_refresh_token(user),
            access_token=create_access_token(user),
        )
