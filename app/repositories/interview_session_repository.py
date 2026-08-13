from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview_session import (
    InterviewSession,
)


class InterviewSessionRepository:

    async def create(
        self,
        db: AsyncSession,
        session: InterviewSession,
    ) -> InterviewSession:

        db.add(session)

        await db.commit()

        await db.refresh(session)

        return session

    async def get_by_id(
        self,
        db: AsyncSession,
        session_id: str,
    ) -> InterviewSession | None:

        result = await db.execute(
            select(InterviewSession).where(
                InterviewSession.id == session_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_active_session(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> InterviewSession | None:

        result = await db.execute(
            select(InterviewSession)
            .where(
                InterviewSession.user_id == user_id,
                InterviewSession.status == "ACTIVE",
            )
            .order_by(
                InterviewSession.created_at.desc(),
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        db: AsyncSession,
        session: InterviewSession,
    ) -> InterviewSession:

        await db.commit()

        await db.refresh(session)

        return session
    
    async def delete(
        self,
        db: AsyncSession,
        session: InterviewSession,
    ) -> None:

        await db.delete(session)

        await db.commit()
        
    async def increment_answered_questions(
        self,
        db: AsyncSession,
        session: InterviewSession,
    ) -> InterviewSession:

        session.answered_questions += 1

        if (
            session.answered_questions
            >= session.total_questions
        ):
            session.status = "COMPLETED"

        await db.commit()

        await db.refresh(session)

        return session    
    
    async def get_completed_sessions_count(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> int:

        result = await db.execute(
            select(
                InterviewSession,
            ).where(
                InterviewSession.user_id
                == user_id,
                InterviewSession.status
                == "COMPLETED",
            )
        )

        return len(
            result.scalars().all()
        )


    async def get_total_sessions_count(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> int:

        result = await db.execute(
            select(
                InterviewSession,
            ).where(
                InterviewSession.user_id
                == user_id,
            )
        )

        return len(
            result.scalars().all()
        )


    async def get_active_sessions_count(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> int:

        result = await db.execute(
            select(
                InterviewSession,
            ).where(
                InterviewSession.user_id
                == user_id,
                InterviewSession.status
                == "ACTIVE",
            )
        )

        return len(
            result.scalars().all()
        )
        
    async def get_recent_sessions(
        self,
        db: AsyncSession,
        user_id: str,
        limit: int = 5,
    ) -> list[InterviewSession]:

        result = await db.execute(
            select(
                InterviewSession,
            )
            .where(
                InterviewSession.user_id
                == user_id,
            )
            .order_by(
                InterviewSession.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )     