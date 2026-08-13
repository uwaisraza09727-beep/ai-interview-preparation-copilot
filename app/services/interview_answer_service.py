from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gemini_answer_evaluator import (
    GeminiAnswerEvaluator,
)

from app.models.interview_answer import (
    InterviewAnswer,
)

from app.repositories.interview_answer_repository import (
    InterviewAnswerRepository,
)

from app.repositories.interview_question_repository import (
    InterviewQuestionRepository,
)
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)


class InterviewAnswerService:

    def __init__(self):

        self.answer_evaluator = (
            GeminiAnswerEvaluator()
        )

        self.answer_repository = (
            InterviewAnswerRepository()
        )

        self.question_repository = (
            InterviewQuestionRepository()
        )
        
        self.session_repository = (
            InterviewSessionRepository()
        )

    async def evaluate_answer(
        self,
        db: AsyncSession,
        user_id: str,
        interview_question_id: str,
        answer: str,
    ) -> InterviewAnswer:

        question = (
            await self.question_repository.get_by_id(
                db,
                interview_question_id,
            )
        )

        if not question:

            raise ValueError(
                "Interview question not found"
            )

        if str(question.user_id) != user_id:
            
            raise ValueError(
                "Access Denied"
            )

        existing_answer = (
            await self.answer_repository.get_by_question_id(
                db,
                question.id,
            )
        )

        if existing_answer:

            raise ValueError(
                "Answer already submitted for this question"
            )
            
        await db.rollback()    
            
        result = (
            await self.answer_evaluator.evaluate_answer(
                question.question,
                answer,
            )
        )

        interview_answer = InterviewAnswer(
            user_id=user_id,
            interview_question_id=question.id,
            answer=answer,
            score=result.score,
            feedback=result.feedback,
            strengths=result.strengths,
            improvements=result.improvements,
            overall_result=result.overall_result,
        )

        saved_answer = (
            await self.answer_repository.create(
                db,
                interview_answer,
            )
        )
        session = (
            await self.session_repository
            .get_active_session(
                db,
                user_id,
            )
        )

        if session:

            await self.session_repository.increment_answered_questions(
                db,
                session,
            )

        return saved_answer

    async def get_my_answers(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[InterviewAnswer]:

        return await self.answer_repository.get_all_by_user(
            db,
            user_id,
        )

    async def get_answer(
        self,
        db: AsyncSession,
        answer_id: str,
        user_id: str,
    ) -> InterviewAnswer:

        answer = (
            await self.answer_repository.get_by_id(
                db,
                answer_id,
            )
        )

        if not answer:

            raise ValueError(
                "Answer not found"
            )

        if str(answer.user_id) != user_id:

            raise ValueError(
                "Access denied"
            )

        return answer

    async def delete_answer(
        self,
        db: AsyncSession,
        answer_id: str,
        user_id: str,
    ) -> None:

        answer = (
            await self.answer_repository.get_by_id(
                db,
                answer_id,
            )
        )

        if not answer:

            raise ValueError(
                "Answer not found"
            )

        if str(answer.user_id) != user_id:

            raise ValueError(
                "Access denied"
            )

        await self.answer_repository.delete(
            db,
            answer,
        )
        
    async def get_performance(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> dict:

        answers = (
            await self.answer_repository
            .get_all_by_user(
                db,
                user_id,
            )
        )

        if not answers:
            return {
                "total_answers": 0,
                "average_score": 0,
            }

        average_score = (
            await self.answer_repository
            .get_average_score(
                db,
                user_id,
            )
        )

        return {
            "total_answers": len(answers),
            "average_score": round(
                float(average_score or 0),
                2,
            ),
        }