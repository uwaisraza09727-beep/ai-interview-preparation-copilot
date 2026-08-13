from pydantic import BaseModel


class InterviewPerformanceResponse(
    BaseModel,
):

    highest_score: int

    lowest_score: int

    average_score: float