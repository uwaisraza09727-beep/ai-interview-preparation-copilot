from pathlib import Path

from fastapi import UploadFile

from app.core.constants.upload import (
    ALLOWED_FILE_TYPES,
    MAX_FILE_SIZE,
)


async def validate_resume_file(
    file: UploadFile,
) -> None:

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_FILE_TYPES:
        raise ValueError(
            "Only PDF and DOCX files are allowed."
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise ValueError(
            "File size must not exceed 10 MB."
        )

    await file.seek(0)