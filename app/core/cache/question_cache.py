from typing import Any

from redis.exceptions import RedisError

from app.core.database.redis import redis_client


class QuestionCache:

    PREFIX = "interview_questions"

    @classmethod
    def _build_key(
        cls,
        user_id: str,
        resume_id: str,
        job_description_id: str,
        category: str,
        difficulty: str,
        question_count: int,
    ) -> str:

        return (
            f"{cls.PREFIX}:"
            f"{user_id}:"
            f"{resume_id}:"
            f"{job_description_id}:"
            f"{category}:"
            f"{difficulty}:"
            f"{question_count}"
        )

    @classmethod
    async def get(
        cls,
        user_id: str,
        resume_id: str,
        job_description_id: str,
        category: str,
        difficulty: str,
        question_count: int,
    ) -> Any | None:

        key = cls._build_key(
            user_id,
            resume_id,
            job_description_id,
            category,
            difficulty,
            question_count,
        )

        try:
            return await redis_client.get(key)

        except RedisError:
            return None

    @classmethod
    async def set(
        cls,
        user_id: str,
        resume_id: str,
        job_description_id: str,
        category: str,
        difficulty: str,
        question_count: int,
        value: str,
        expire_seconds: int = 300,
    ) -> bool:

        key = cls._build_key(
            user_id,
            resume_id,
            job_description_id,
            category,
            difficulty,
            question_count,
        )

        try:
            return await redis_client.set(
                key,
                value,
                ex=expire_seconds,
            )

        except RedisError:
            return False

    @classmethod
    async def delete(
        cls,
        user_id: str,
        resume_id: str,
        job_description_id: str,
        category: str,
        difficulty: str,
        question_count: int,
    ) -> bool:

        key = cls._build_key(
            user_id,
            resume_id,
            job_description_id,
            category,
            difficulty,
            question_count,
        )

        try:
            await redis_client.delete(key)
            return True

        except RedisError:
            return False