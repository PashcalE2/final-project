import jwt
from datetime import datetime, timedelta

from src.core.models import UserModelSchema
from src.settings import Settings, get_settings
from src.exception import TokenException, BrokenToken


settings: Settings = get_settings()
ALGORITHM = "HS256"


def create_refresh_token(user: UserModelSchema) -> str:
    to_encode = user.model_dump(exclude={"password"})
    expire = datetime.now() + timedelta(
        minutes=settings.backend.refresh_token_expiration_minutes
    )
    to_encode.update({"exp": int(expire.timestamp())})

    refresh_jwt = jwt.encode(
        payload=to_encode,
        key=settings.backend.refresh_secret,
        algorithm=ALGORITHM,
    )

    return refresh_jwt


def decode_refresh_token(token: str) -> dict:
    try:
        data: dict = jwt.decode(
            jwt=token,
            key=settings.backend.refresh_secret,
            algorithms=(ALGORITHM,),
            verify=True,
        )
    except jwt.exceptions.PyJWTError as e:
        raise TokenException(msg=str(e))

    if data.get("id") is None:
        raise BrokenToken()
    return data


def create_access_token(user: UserModelSchema) -> str:
    to_encode = user.model_dump(exclude={"password"})
    expire = datetime.now() + timedelta(
        minutes=settings.backend.access_token_expiration_minutes
    )
    to_encode.update({"exp": int(expire.timestamp())})

    access_jwt = jwt.encode(
        payload=to_encode,
        key=settings.backend.access_secret,
        algorithm=ALGORITHM,
    )

    return access_jwt


def decode_access_token(token: str) -> dict:
    try:
        data: dict = jwt.decode(
            jwt=token,
            key=settings.backend.access_secret,
            algorithms=(ALGORITHM,),
            verify=True,
        )
    except jwt.exceptions.PyJWTError as e:
        raise TokenException(msg=str(e))

    if data.get("id") is None:
        raise BrokenToken()
    return data
