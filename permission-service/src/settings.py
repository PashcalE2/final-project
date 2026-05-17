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


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RABBITMQ_",
        extra="ignore",
        case_sensitive=False,
    )

    host: str
    port: int
    user: str
    password: str

    @computed_field
    @property
    def dsn(self) -> AmqpDsn:
        return AmqpDsn(f"amqp://{self.user}:{self.password}@{self.host}:{self.port}")


class Settings(BaseSettings):
    auth_service: AuthServiceSettings = AuthServiceSettings()
    backend: BackendSettings = BackendSettings()
    db: DatabaseSettings = DatabaseSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()


settings = Settings()
