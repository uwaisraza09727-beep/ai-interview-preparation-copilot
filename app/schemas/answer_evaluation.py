from pydantic import BaseModel


class AnswerEvaluation(BaseModel):

    score: int

    feedback: str

    strengths: str

    improvements: str

    overall_result: str