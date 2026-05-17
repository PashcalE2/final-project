from datetime import time
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, PostgresDsn, RedisDsn


class BackendSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BACKEND_",
        extra="ignore",
        case_sensitive=False,
    )

    workers: int
    refresh_secret: str
    access_secret: str
    refresh_token_expiration_minutes: int
    access_token_expiration_minutes: int


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        extra="ignore",
        case_sensitive=False,
    )

    name: str
    host: str
    port: int
    user: str
    password: str

    @computed_field
    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        extra="ignore",
        case_sensitive=False,
    )

    password: str
    host: str
    port: int
    expiration_at: time
    max_connections: int = 10
    decode_responses: bool = True

    @computed_field
    @property
    def dsn(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class Settings(BaseSettings):
    backend: BackendSettings = BackendSettings()
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
