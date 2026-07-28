from pydantic import BaseModel


class MatchResult(BaseModel):

    score: float

    matched_keywords: list[str]

    missing_keywords: list[str]