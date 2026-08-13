from pydantic import BaseModel


class InterviewStatisticsResponse(
    BaseModel,
):

    total_sessions: int

    completed_sessions: int

    active_sessions: int

    total_answers: int

    average_score: float