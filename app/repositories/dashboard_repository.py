from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_description import JobDescription
from app.models.match_result import MatchResult
from app.models.resume import Resume


class DashboardRepository:

    async def get_dashboard_stats(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> dict:

        total_resumes = await db.scalar(
            select(func.count()).where(
                Resume.user_id == user_id,
            )
        )

        total_job_descriptions = await db.scalar(
            select(func.count()).where(
                JobDescription.user_id == user_id,
            )
        )

        total_matches = await db.scalar(
            select(func.count()).where(
                MatchResult.user_id == user_id,
            )
        )

        average_match_score = await db.scalar(
            select(
                func.avg(
                    MatchResult.overall_score,
                )
            ).where(
                MatchResult.user_id == user_id,
            )
        )

        highest_match_score = await db.scalar(
            select(
                func.max(
                    MatchResult.overall_score,
                )
            ).where(
                MatchResult.user_id == user_id,
            )
        )

        return {
            "total_resumes": total_resumes or 0,
            "total_job_descriptions": total_job_descriptions or 0,
            "total_matches": total_matches or 0,
            "average_match_score": round(
                average_match_score or 0,
                2,
            ),
            "highest_match_score": round(
                highest_match_score or 0,
                2,
            ),
        }