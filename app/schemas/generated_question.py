from pydantic import BaseModel


class GeneratedQuestion(BaseModel):

    question: str

    question_type: str


class GeneratedQuestions(BaseModel):

    questions: list[GeneratedQuestion]