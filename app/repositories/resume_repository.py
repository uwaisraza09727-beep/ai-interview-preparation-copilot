from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume


class ResumeRepository:

    async def create(
        self,
        db: AsyncSession,
        resume: Resume,
    ) -> Resume:

        db.add(resume)

        await db.commit()

        await db.refresh(resume)

        return resume
    
    async def get_all_by_user(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[Resume]:

        result = await db.execute(
            select(Resume).where(
                Resume.user_id == user_id
            )
        )

        return list(result.scalars().all())
    
    async def get_by_id(
        self,
        db: AsyncSession,
        resume_id: str,
    ) -> Resume | None:

        result = await db.execute(
            select(Resume).where(
                Resume.id == resume_id
            )
        )

        return result.scalar_one_or_none()
    
    async def delete(
        self,
        db: AsyncSession,
        resume: Resume,
    ) -> None:

        await db.delete(resume)

        await db.commit()