from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from app.models.interview_answer import (
    InterviewAnswer,
)


class InterviewAnswerRepository:

    async def create(
        self,
        db: AsyncSession,
        interview_answer: InterviewAnswer,
    ) -> InterviewAnswer:

        db.add(interview_answer)

        await db.commit()

        await db.refresh(interview_answer)

        return interview_answer

    async def get_by_id(
        self,
        db: AsyncSession,
        answer_id: str,
    ) -> InterviewAnswer | None:

        result = await db.execute(
            select(InterviewAnswer).where(
                InterviewAnswer.id == answer_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[InterviewAnswer]:

        result = await db.execute(
            select(InterviewAnswer)
            .where(
                InterviewAnswer.user_id == user_id,
            )
            .order_by(
                InterviewAnswer.created_at.desc(),
            )
        )

        return list(
            result.scalars().all()
        )
        
    async def get_by_question_id(
        self,
        db: AsyncSession,
        question_id: str,
    ) -> InterviewAnswer | None:

        result = await db.execute(
            select(
                InterviewAnswer,
            ).where(
                InterviewAnswer.interview_question_id == question_id,
            )
        )

        return result.scalar_one_or_none()     

    async def delete(
        self,
        db: AsyncSession,
        interview_answer: InterviewAnswer,
    ) -> None:

        await db.delete(interview_answer)

        await db.commit()
        
    async def get_average_score(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> float | None:

        result = await db.execute(
            select(
                func.avg(
                    InterviewAnswer.score,
                )
            ).where(
                InterviewAnswer.user_id
                == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_total_answers(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> int:

        result = await db.execute(
            select(
                InterviewAnswer,
            ).where(
                InterviewAnswer.user_id
                == user_id,
            )
        )

        return len(
            result.scalars().all()
        )  
        
    async def get_score_statistics(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> dict:

        result = await db.execute(
            select(
                func.max(
                    InterviewAnswer.score,
                ),
                func.min(
                    InterviewAnswer.score,
                ),
                func.avg(
                    InterviewAnswer.score,
                ),
            ).where(
                InterviewAnswer.user_id
                == user_id,
            )
        )

        highest_score, lowest_score, average_score = (
            result.one()
        )

        return {
            "highest_score":
                int(
                    highest_score or 0
                ),

            "lowest_score":
                int(
                    lowest_score or 0
                ),

            "average_score":
                round(
                    float(
                        average_score or 0
                    ),
                    2,
                ),
        }      