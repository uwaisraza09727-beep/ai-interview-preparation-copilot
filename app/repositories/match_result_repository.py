from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.match_result import MatchResult


class MatchResultRepository:

    async def create(
        self,
        db: AsyncSession,
        match_result: MatchResult,
    ) -> MatchResult:

        db.add(match_result)

        await db.commit()

        await db.refresh(match_result)

        return match_result

    async def get_by_id(
        self,
        db: AsyncSession,
        match_result_id: str,
    ) -> MatchResult | None:

        result = await db.execute(
            select(MatchResult).where(
                MatchResult.id == match_result_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[MatchResult]:

        result = await db.execute(
            select(MatchResult).where(
                MatchResult.user_id == user_id,
            )
        )

        return list(
            result.scalars().all()
        )

    async def delete(
        self,
        db: AsyncSession,
        match_result: MatchResult,
    ) -> None:

        await db.delete(match_result)

        await db.commit()