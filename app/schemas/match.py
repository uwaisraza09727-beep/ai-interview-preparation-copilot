from pydantic import BaseModel


class MatchResponse(BaseModel):
    overall_score: float

    matched_skills: list[str]

    missing_skills: list[str]

    matched_keywords: list[str]

    missing_keywords: list[str]