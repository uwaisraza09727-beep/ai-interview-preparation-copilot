import uuid

from pydantic import (
    BaseModel,
)


class StartInterviewRequest(BaseModel):

    resume_id: str

    job_description_id: str

    total_questions: int


class InterviewSessionResponse(BaseModel):

    id: uuid.UUID

    resume_id: uuid.UUID

    job_description_id: uuid.UUID

    total_questions: int

    answered_questions: int

    status: str

    model_config = {
        "from_attributes": True,
    }