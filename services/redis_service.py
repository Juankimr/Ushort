from dataclasses import dataclass

import redis


@dataclass
class RedisService:
    _redis: redis.Redis

    def set(self, key: str, value):
        return self._redis.hset(name=key, key=key, value=value)

    def len(self, key: str):
        return self._redis.hlen(key)

    def get(self, key: str):
        return self._redis.hget(name=key, key=key)

    def get_all(self, key: str):
        return self._redis.hgetall(key)
