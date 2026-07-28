from app.ai.matcher import ResumeMatcher
from app.repositories.resume_repository import ResumeRepository
from app.repositories.job_description_repository import JobDescriptionRepository


class MatchingService:

    def __init__(self):
        self.matcher = ResumeMatcher()
        self.resume_repository = ResumeRepository()
        self.job_description_repository = JobDescriptionRepository()
        
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
            raise ValueError("Resume not found")

        job_description = await self.job_description_repository.get_by_id(
            db,
            job_description_id,
        )

        if not job_description:
            raise ValueError("Job Description not found")

        if str(resume.user_id) != user_id:
            raise ValueError("Access denied")

        if str(job_description.user_id) != user_id:
            raise ValueError("Access denied")

        return self.matcher.calculate_match(
            resume.resume_text,
            job_description.jd_text,
        )    