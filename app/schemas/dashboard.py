from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_resumes: int

    total_job_descriptions: int

    total_matches: int

    average_match_score: float

    highest_match_score: float