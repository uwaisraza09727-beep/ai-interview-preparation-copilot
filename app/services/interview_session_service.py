from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview_session import (
    InterviewSession,
)

from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)

from app.repositories.interview_question_repository import (
    InterviewQuestionRepository,
)
from app.models.interview_question import (
    InterviewQuestion,
)
from app.repositories.interview_answer_repository import (
    InterviewAnswerRepository,
)


class InterviewSessionService:

    def __init__(self):

        self.session_repository = (
            InterviewSessionRepository()
        )

        self.question_repository = (
            InterviewQuestionRepository()
        )
        
        self.answer_repository = (
            InterviewAnswerRepository()
        )

    async def start_session(
        self,
        db: AsyncSession,
        user_id: str,
        resume_id: str,
        job_description_id: str,
    ) -> InterviewSession:

        existing = (
            await self.session_repository
            .get_active_session(
                db,
                user_id,
            )
        )

        if existing:

            raise ValueError(
                "An interview session is already active."
            )

        questions = (
            await self.question_repository
            .get_all_by_resume_and_job(
                db,
                user_id,
                resume_id,
                job_description_id,
            )
        )

        if not questions:

            raise ValueError(
                "Generate interview questions first."
            )

        session = InterviewSession(
            user_id=user_id,
            resume_id=resume_id,
            job_description_id=job_description_id,
            total_questions=len(
                questions
            ),
            answered_questions=0,
            status="ACTIVE",
        )

        return await (
            self.session_repository.create(
                db,
                session,
            )
        )
        
    async def get_active_session(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> InterviewSession:

        session = (
            await self.session_repository
            .get_active_session(
                db,
                user_id,
            )
        )

        if not session:

            raise ValueError(
                "No active interview session."
            )

        return session


    async def finish_session(
        self,
        db: AsyncSession,
        user_id: str,
    ):

        session = (
            await self.get_active_session(
                db,
                user_id,
            )
        )

        session.status = "COMPLETED"

        await self.session_repository.update(
            db,
            session,
        )

        return session    
    
    async def get_current_question(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> InterviewQuestion:

        session = (
            await self.get_active_session(
                db,
                user_id,
            )
        )

        questions = (
            await self.question_repository
            .get_by_resume_and_job(
                db,
                session.resume_id,
                session.job_description_id,
            )
        )

        if not questions:

            raise ValueError(
                "No interview questions found."
            )

        if (
            session.answered_questions
            >= len(questions)
        ):

            raise ValueError(
                "Interview completed."
            )

        return questions[
            session.answered_questions
        ]
        
    async def get_dashboard(
        self,
        db: AsyncSession,
        user_id: str,
    ):

        session = (
            await self.get_active_session(
                db,
                user_id,
            )
        )

        remaining_questions = (
            session.total_questions
            - session.answered_questions
        )

        completion_percentage = (
            session.answered_questions
            / session.total_questions
        ) * 100

        return {
            "total_questions":
                session.total_questions,

            "answered_questions":
                session.answered_questions,

            "remaining_questions":
                remaining_questions,

            "completion_percentage":
                round(
                    completion_percentage,
                    2,
                ),

            "status":
                session.status,
        }   
        
    async def get_statistics(
        self,
        db: AsyncSession,
        user_id: str,
    ):

        total_sessions = (
            await self.session_repository
            .get_total_sessions_count(
                db,
                user_id,
            )
        )

        completed_sessions = (
            await self.session_repository
            .get_completed_sessions_count(
                db,
                user_id,
            )
        )

        active_sessions = (
            await self.session_repository
            .get_active_sessions_count(
                db,
                user_id,
            )
        )

        total_answers = (
            await self.answer_repository
            .get_total_answers(
                db,
                user_id,
            )
        )

        average_score = (
            await self.answer_repository
            .get_average_score(
                db,
                user_id,
            )
        )

        return {

            "total_sessions":
                total_sessions,

            "completed_sessions":
                completed_sessions,

            "active_sessions":
                active_sessions,

            "total_answers":
                total_answers,

            "average_score":
                round(
                    average_score,
                    2,
                ),
        } 
        
    async def get_summary(
        self,
        db: AsyncSession,
        user_id: str,
    ):

        total_sessions = (
            await self.session_repository
            .get_total_sessions_count(
                db,
                user_id,
            )
        )

        completed_sessions = (
            await self.session_repository
            .get_completed_sessions_count(
                db,
                user_id,
            )
        )

        active_sessions = (
            await self.session_repository
            .get_active_sessions_count(
                db,
                user_id,
            )
        )

        total_answers = (
            await self.answer_repository
            .get_total_answers(
                db,
                user_id,
            )
        )

        average_score = (
            await self.answer_repository
            .get_average_score(
                db,
                user_id,
            )
        )

        if total_sessions > 0:

            completion_rate = (
                completed_sessions
                / total_sessions
            ) * 100

        else:

            completion_rate = 0.0

        return {
            "total_sessions":
                total_sessions,

            "completed_sessions":
                completed_sessions,

            "active_sessions":
                active_sessions,

            "total_answers":
                total_answers,

            "average_score":
                round(
                    average_score,
                    2,
                ),

            "completion_rate":
                round(
                    completion_rate,
                    2,
                ),
        }  
        
    async def get_recent_sessions(
        self,
        db: AsyncSession,
        user_id: str,
        limit: int = 5,
    ) -> list[InterviewSession]:

        return await (
            self.session_repository
            .get_recent_sessions(
                db,
                user_id,
                limit,
            )
        )          