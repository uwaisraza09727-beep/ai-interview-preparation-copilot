from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview_question import InterviewQuestion




class InterviewQuestionRepository:

    async def create(
        self,
        db: AsyncSession,
        question: InterviewQuestion,
    ) -> InterviewQuestion:

        db.add(question)

        await db.commit()

        await db.refresh(question)

        return question

    async def create_many(
        self,
        db: AsyncSession,
        questions: list[InterviewQuestion],
    ) -> list[InterviewQuestion]:

        db.add_all(questions)

        await db.commit()

        for question in questions:
            await db.refresh(question)

        return questions

    async def get_by_id(
        self,
        db: AsyncSession,
        question_id: str,
    ) -> InterviewQuestion | None:

        result = await db.execute(
            select(InterviewQuestion).where(
                InterviewQuestion.id == question_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[InterviewQuestion]:

        result = await db.execute(
            select(InterviewQuestion).where(
                InterviewQuestion.user_id == user_id,
            )
            .order_by(
                InterviewQuestion.created_at.desc()
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_all_by_resume_and_job(
        self,
        db: AsyncSession,
        user_id: str,
        resume_id: str,
        job_description_id: str,
    ) -> list[InterviewQuestion]:

        result = await db.execute(
            select(
                InterviewQuestion,
            ).where(
                InterviewQuestion.user_id == user_id,
                InterviewQuestion.resume_id == resume_id,
                InterviewQuestion.job_description_id
                == job_description_id,
            )
        )

        return list(
            result.scalars().all()
        )
        
    async def get_existing_questions(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[str]:

        result = await db.execute(
            select(
                InterviewQuestion.question,
            ).where(
                InterviewQuestion.user_id == user_id,
            )
        )

        return list(
            result.scalars().all()
        )    
        
    async def delete(
        self,
        db: AsyncSession,
        question: InterviewQuestion,
    ) -> None:

        await db.delete(
            question,
        )

        await db.commit()    
        
    async def get_by_resume_and_job(
        self,
        db: AsyncSession,
        resume_id: str,
        job_description_id: str,
    ) -> list[InterviewQuestion]:

        result = await db.execute(
            select(
                InterviewQuestion,
            )
            .where(
                InterviewQuestion.resume_id
                == resume_id,
                InterviewQuestion.job_description_id
                == job_description_id,
            )
            .order_by(
                InterviewQuestion.created_at.asc(),
            )
        )

        return list(
            result.scalars().all()
        )    
