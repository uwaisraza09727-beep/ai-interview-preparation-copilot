from app.ai.matcher import ResumeMatcher

from app.models.match_result import MatchResult

from app.repositories.resume_repository import ResumeRepository
from app.repositories.job_description_repository import (
    JobDescriptionRepository,
)
from app.repositories.match_result_repository import (
    MatchResultRepository,
)


class MatchingService:

    def __init__(self):
        self.matcher = ResumeMatcher()
        self.resume_repository = ResumeRepository()
        self.job_description_repository = JobDescriptionRepository()
        self.match_result_repository = MatchResultRepository()

    async def match_resume_with_jd(
        self,
        db,
        resume_id: str,
        job_description_id: str,
        user_id: str,
    ):

        resume = await self.resume_repository.get_by_id(
            db,
            resume_id,
        )

        if not resume:
            raise ValueError(
                "Resume not found"
            )

        job_description = await self.job_description_repository.get_by_id(
            db,
            job_description_id,
        )

        if not job_description:
            raise ValueError(
                "Job Description not found"
            )

        if str(resume.user_id) != user_id:
            raise ValueError(
                "Access denied"
            )

        if str(job_description.user_id) != user_id:
            raise ValueError(
                "Access denied"
            )

        result = self.matcher.calculate_match(
            resume.resume_text,
            job_description.jd_text,
        )

        match_result = MatchResult(
            user_id=user_id,
            resume_id=resume.id,
            job_description_id=job_description.id,
            overall_score=result["overall_score"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            matched_keywords=result["matched_keywords"],
            missing_keywords=result["missing_keywords"],
        )

        saved_result = await self.match_result_repository.create(
            db,
            match_result,
        )

        return saved_result

    async def get_match_history(
        self,
        db,
        user_id: str,
    ):

        return await self.match_result_repository.get_all_by_user(
            db,
            user_id,
        )

    async def get_match(
        self,
        db,
        match_result_id: str,
        user_id: str,
    ):

        match = await self.match_result_repository.get_by_id(
            db,
            match_result_id,
        )

        if not match:
            raise ValueError(
                "Match not found"
            )

        if str(match.user_id) != user_id:
            raise ValueError(
                "Access denied"
            )

        return match
    
    async def delete_match(
        self,
        db,
        match_result_id: str,
        user_id: str,
    ) -> None:

        match = await self.match_result_repository.get_by_id(
            db,
            match_result_id,
        )

        if not match:
            raise ValueError(
                "Match result not found"
            )

        if str(match.user_id) != user_id:
            raise ValueError(
                "Access denied"
            )

        await self.match_result_repository.delete(
            db,
            match,
        )