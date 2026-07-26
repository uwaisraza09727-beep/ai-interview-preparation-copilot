from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.settings import settings
from app.models.resume import Resume
from app.repositories.resume_repository import ResumeRepository
from app.utils.file_validator import validate_resume_file

from app.utils.parsers.pdf_parser import extract_pdf_text
from app.utils.parsers.docx_parser import extract_docx_text

from app.utils.parsers.parser import (
    extract_resume_text,
)
from app.ai.resume_parser import ResumeParser


class ResumeService:

    def __init__(self):
        self.resume_repository = ResumeRepository()

    async def upload_resume(
        self,
        db: AsyncSession,
        user_id: str,
        file: UploadFile,
    ) -> Resume:
        
        await validate_resume_file(file)
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        extension = Path(file.filename).suffix

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
        
        resume_text = extract_resume_text(
           str(file_path),
           extension,
        )
        
        parser = ResumeParser()

        parsed_resume = parser.parse(
            resume_text,
        )

        print(parsed_resume)
        
        
        resume = Resume(
            user_id=user_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_size=len(content),
            file_type=extension,
            upload_status="uploaded",
            resume_text=resume_text,
        )

        return await self.resume_repository.create(
            db,
            resume,
        )
        
    async def get_my_resumes(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[Resume]:

        return await self.resume_repository.get_all_by_user(
            db,
            user_id,
        )
        
    async def get_resume(
        self,
        db: AsyncSession,
        resume_id: str,
        user_id: str,
    ) -> Resume:

        resume = await self.resume_repository.get_by_id(
            db,
            resume_id,
        )

        if not resume:
            raise ValueError("Resume not found")

        if str(resume.user_id) != user_id:
            raise ValueError("Access denied")

        return resume        
    
    async def delete_resume(
        self,
        db: AsyncSession,
        resume_id: str,
        user_id: str,
    ) -> None:

        resume = await self.get_resume(
            db,
            resume_id,
            user_id,
        )

        file_path = Path(resume.file_path)

        if file_path.exists():
            file_path.unlink()

        await self.resume_repository.delete(
            db,
            resume,
        )