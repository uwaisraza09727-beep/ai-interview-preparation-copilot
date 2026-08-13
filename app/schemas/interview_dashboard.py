from pydantic import BaseModel


class InterviewDashboardResponse(
    BaseModel,
):

    total_questions: int

    answered_questions: int

    remaining_questions: int

    completion_percentage: float

    status: str