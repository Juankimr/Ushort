import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    redis_url: AnyUrl = os.environ.get("REDIS_URL", "redis://redis")
    redis_password: str = os.getenv("REDIS_PASSWORD", "redis_pass")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    up: str = os.getenv("UP", "up")
    down: str = os.getenv("DOWN", "down")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()


settings = get_settings()