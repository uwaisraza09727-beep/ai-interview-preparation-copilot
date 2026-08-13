from pydantic import BaseModel, Field


class InterviewQuestionGenerateRequest(BaseModel):

    resume_id: str

    job_description_id: str

    category: str = Field(
        default="technical",
        min_length=2,
        max_length=50,
    )

    difficulty: str = Field(
        default="medium",
        min_length=2,
        max_length=30,
    )

    question_count: int = Field(
        default=10,
        ge=1,
        le=20,
    )