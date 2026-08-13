from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.settings import settings
from app.models.job_description import JobDescription
from app.repositories.job_description_repository import (
    JobDescriptionRepository,
)

from app.utils.file_validator import validate_resume_file

from app.utils.parsers.parser import (
    extract_resume_text,
)


class JobDescriptionService:

    def __init__(self):
        self.job_description_repository = JobDescriptionRepository()

    async def upload_job_description(
        self,
        db: AsyncSession,
        user_id: str,
        file: UploadFile,
    ) -> JobDescription:

        await validate_resume_file(file)

        upload_dir = Path(
            settings.job_description_upload_dir,
        )

        upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        extension = Path(
            file.filename,
        ).suffix

        stored_filename = (
            f"{uuid4()}{extension}"
        )

        file_path = upload_dir / stored_filename

        content = await file.read()

        with open(
            file_path,
            "wb",
        ) as buffer:
            buffer.write(content)

        jd_text = extract_resume_text(
            str(file_path),
            extension,
        )

        job_description = JobDescription(
            user_id=user_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_size=len(content),
            file_type=extension,
            upload_status="uploaded",
            jd_text=jd_text,
        )

        return await self.job_description_repository.create(
            db,
            job_description,
        )

    async def get_my_job_descriptions(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[JobDescription]:

        return await self.job_description_repository.get_all_by_user(
            db,
            user_id,
        )

    async def get_job_description(
        self,
        db: AsyncSession,
        job_description_id: str,
        user_id: str,
    ) -> JobDescription:

        job_description = (
            await self.job_description_repository.get_by_id(
                db,
                job_description_id,
            )
        )

        if not job_description:
            raise ValueError(
                "Job description not found"
            )

        if str(job_description.user_id) != user_id:
            raise ValueError(
                "Access denied"
            )

        return job_description

    async def delete_job_description(
        self,
        db: AsyncSession,
        job_description_id: str,
        user_id: str,
    ) -> None:

        job_description = (
            await self.get_job_description(
                db,
                job_description_id,
                user_id,
            )
        )

        file_path = Path(
            job_description.file_path,
        )

        if file_path.exists():
            file_path.unlink()

        await self.job_description_repository.delete(
            db,
            job_description,
        )
        
    async def create_from_text(
        self,
        db: AsyncSession,
        user_id: str,
        title: str,
        jd_text: str,
    ) -> JobDescription:

        if not jd_text.strip():
            raise ValueError(
                "Job description text cannot be empty."
            )

        job_description = JobDescription(
            user_id=user_id,
            original_filename=title,
            stored_filename=f"text-{uuid4()}.txt",
            file_path="",
            file_size=len(
                jd_text.encode("utf-8")
            ),
            file_type="text",
            upload_status="uploaded",
            jd_text=jd_text.strip(),
        )

        return await self.job_description_repository.create(
            db,
            job_description,
        )    