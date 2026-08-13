from pydantic import BaseModel, Field
import uuid


class InterviewAnswerRequest(BaseModel):

    interview_question_id: str = Field(
        ...,
        description="Interview Question UUID",
    )

    answer: str = Field(
        ...,
        min_length=10,
        max_length=5000,
    )


class InterviewAnswerResponse(BaseModel):

    id:  uuid.UUID

    interview_question_id: uuid.UUID

    answer: str

    score: int

    feedback: str

    strengths: str

    improvements: str

    overall_result: str

    model_config = {
        "from_attributes": True,
    }
    
class InterviewAnswerPerformanceResponse(
    BaseModel
):

    total_answers: int

    average_score: float    