from typing import Optional

from app.core.database.redis import redis_client


class CacheService:

    async def set(
        self,
        key: str,
        value: str,
        expire_seconds: int = 300,
    ) -> bool:

        return await redis_client.set(
            key,
            value,
            ex=expire_seconds,
        )

    async def get(
        self,
        key: str,
    ) -> Optional[str]:

        return await redis_client.get(
            key
        )

    async def delete(
        self,
        key: str,
    ) -> int:

        return await redis_client.delete(
            key
        )


cache_service = CacheService()