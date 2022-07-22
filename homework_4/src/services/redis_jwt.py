import redis

from src.core import config
from pydantic import BaseModel

blocked_access_tokens = redis.Redis(host=config.REDIS_HOST, port=9000, db=1)
active_refresh_tokens = redis.Redis(host=config.REDIS_HOST, port=9000, db=2)

__all__ = ("JwtCache",)


class JwtCache(BaseModel):
    @staticmethod
    def add_to_active_refresh(user_uuid: str, refresh_jti: str) -> None:
        """Добавляем активный в refresh_token в redis."""
        active_refresh_tokens.rpush(user_uuid, refresh_jti)

    @staticmethod
    def logout(user_uuid: str, access_jti: str, refresh_jti: str) -> None:
        """Вносит access_token в список заблокированных, а refresh_token удаляет из активных."""
        blocked_access_tokens.rpush(user_uuid, access_jti)
        active_refresh_tokens.lrem(user_uuid, 1, refresh_jti)

    @staticmethod
    def logout_all(user_uuid: str, access_jti: str) -> None:
        """Удаляет все активные refresh_token для определенного user_uuid."""
        blocked_access_tokens.rpush(user_uuid, access_jti)
        active_refresh_tokens.delete(user_uuid)

    @staticmethod
    def is_active_access_token(user_uuid: str, access_jti: str):
        """Проверяет что access_token активен, если нет - бросает исключение."""
        blocked = blocked_access_tokens.lrange(user_uuid, 0, -1)
        if access_jti.encode("utf-8") in blocked:
            raise Exception("token is blocked")

    @staticmethod
    def is_active_refresh_token(user_uuid: str, refresh_jti: str):
        """Проверяет что refresh_token активен, если нет - бросает исключение."""
        active = active_refresh_tokens.lrange(user_uuid, 0, -1)
        if refresh_jti.encode("utf-8") not in active:
            raise Exception("token inactive")
