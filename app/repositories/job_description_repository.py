from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_description import JobDescription


class JobDescriptionRepository:

    async def create(
        self,
        db: AsyncSession,
        job_description: JobDescription,
    ) -> JobDescription:

        db.add(job_description)

        await db.commit()

        await db.refresh(job_description)

        return job_description

    async def get_all_by_user(
        self,
        db: AsyncSession,
        user_id: UUID,
    ) -> list[JobDescription]:

        result = await db.execute(
            select(JobDescription).where(
                JobDescription.user_id == user_id,
            )
        )

        return list(result.scalars().all())

    async def get_by_id(
        self,
        db: AsyncSession,
        jd_id: UUID,
    ) -> JobDescription | None:

        result = await db.execute(
            select(JobDescription).where(
                JobDescription.id == jd_id,
            )
        )

        return result.scalar_one_or_none()

    async def delete(
        self,
        db: AsyncSession,
        job_description: JobDescription,
    ):

        await db.delete(job_description)

        await db.commit()