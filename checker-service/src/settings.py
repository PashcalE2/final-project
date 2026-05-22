from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, PostgresDsn, AmqpDsn


class AuthServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        extra="ignore",
        case_sensitive=False,
    )

    host: str
    port: int
    api_path: str

    @computed_field
    @property
    def get_id_url(self) -> str:
        return f"http://{self.host}:{self.port}{self.api_path}"


class BackendSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BACKEND_",
        extra="ignore",
        case_sensitive=False,
    )

    workers: int
    admin_group_name: str


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        extra="ignore",
        case_sensitive=False,
    )

    user: str
    password: str
    host: str
    port: int
    name: str

    @computed_field
    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RABBITMQ_",
        extra="ignore",
        case_sensitive=False,
    )

    user: str
    password: str
    host: str
    port: int

    @computed_field
    @property
    def dsn(self) -> AmqpDsn:
        return AmqpDsn(f"amqp://{self.user}:{self.password}@{self.host}:{self.port}")


class Settings(BaseSettings):
    auth_service: AuthServiceSettings
    backend: BackendSettings
    db: DatabaseSettings
    rabbitmq: RabbitMQSettings


@lru_cache
def get_settings() -> Settings:
    return Settings(
        auth_service=AuthServiceSettings(),
        backend=BackendSettings(),
        db=DatabaseSettings(),
        rabbitmq=RabbitMQSettings()
    )
