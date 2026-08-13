from pydantic import BaseModel


class AnswerFeedback(BaseModel):

    score: int

    feedback: str

    strengths: str

    improvements: str

    overall_result: str