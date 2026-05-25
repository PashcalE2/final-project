from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from redis.asyncio import Redis
from json import loads as json_loads, dumps as json_dumps

from src.core.repository import AuthRepository
from src.core.models import LoginSchema, UserModelSchema
from src.database.postgres.models import UserModel
from src.database.redis.utils import get_request_expiration_seconds
from src.exception import UserNotFound


class AuthRepositoryImpl(AuthRepository):
    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.session = session
        self.redis = redis

    async def add(self, data: LoginSchema) -> UserModelSchema:
        user = UserModel(login=data.login, password=data.password)
        try:
            self.session.add(user)
            await self.session.flush()
        except:
            raise

        return UserModelSchema(**user.as_dict())

    async def get_user_by_id(self, user_id: int) -> UserModelSchema:
        redis_key = f"user:id={user_id}"
        result = await self.redis.get(redis_key)
        if result is not None:
            return UserModelSchema(**json_loads(result))

        stmt = select(UserModel).where(UserModel.id == user_id).limit(1)

        try:
            response = await self.session.execute(stmt)
            user: UserModel = response.scalar_one()
        except NoResultFound:
            raise UserNotFound()

        user_dict = user.as_dict()
        await self.redis.setex(
            name=redis_key,
            time=get_request_expiration_seconds(),
            value=json_dumps(user_dict),
        )

        return UserModelSchema(**user_dict)

    async def get_user_by_login(self, login: str) -> UserModelSchema:
        redis_key = f"user:login={login}"
        result = await self.redis.get(redis_key)
        if result is not None:
            return UserModelSchema(**json_loads(result))

        stmt = select(UserModel).where(UserModel.login == login).limit(1)

        try:
            response = await self.session.execute(stmt)
            user: UserModel = response.scalar_one()
        except NoResultFound:
            raise UserNotFound()

        user_dict = user.as_dict()
        await self.redis.setex(
            name=redis_key,
            time=get_request_expiration_seconds(),
            value=json_dumps(user_dict),
        )

        return UserModelSchema(**user_dict)
