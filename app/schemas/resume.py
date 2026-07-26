from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    id: UUID
    original_filename: str
    stored_filename: str
    file_size: int
    file_type: str
    upload_status: str
    resume_text: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )