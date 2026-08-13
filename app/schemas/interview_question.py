import uuid

from datetime import datetime

from pydantic import BaseModel


class InterviewQuestionResponse(BaseModel):

    id: uuid.UUID

    user_id: uuid.UUID

    resume_id: uuid.UUID

    job_description_id: uuid.UUID

    question: str

    category: str

    difficulty: str
    
    question_type: str

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }