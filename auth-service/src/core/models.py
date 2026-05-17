from pydantic import BaseModel


class LoginSchema(BaseModel):
    login: str
    password: str


class UserModelSchema(BaseModel):
    id: int
    login: str
    password: str


class TokensPairSchema(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str = "bearer"


class AccessTokenSchema(BaseModel):
    access_token: str


class UserIdSchema(BaseModel):
    id: int


class RefreshTokenSchema(BaseModel):
    refresh_token: str
