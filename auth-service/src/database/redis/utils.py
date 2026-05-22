from datetime import datetime, timedelta

from src.settings import Settings, get_settings


settings: Settings = get_settings()


def get_request_expiration_seconds() -> int:
    now_truncated = datetime.now().replace(microsecond=0)
    expiration_time = now_truncated.replace(
        hour=settings.redis.expiration_at.hour,
        minute=settings.redis.expiration_at.minute,
        second=0,
    )

    if now_truncated >= expiration_time:
        expiration_time += timedelta(days=1)

    seconds = int(expiration_time.timestamp() - now_truncated.timestamp())
    return seconds
