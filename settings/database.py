import redis

from settings.config import settings


def setup_redis() -> redis.Redis:
    redis_c = redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        db=settings.redis_db,
        password=settings.redis_password,
        decode_responses=True,
    )
    return redis_c