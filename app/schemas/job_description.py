from datetime import datetime
import uuid

from pydantic import BaseModel


class JobDescriptionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID

    original_filename: str
    stored_filename: str

    file_path: str
    file_size: int
    file_type: str

    upload_status: str

    jd_text: str | None = None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }