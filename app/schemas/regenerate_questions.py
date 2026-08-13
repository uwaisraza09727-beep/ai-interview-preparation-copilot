from pydantic import BaseModel


class RegenerateQuestionsRequest(BaseModel):

    resume_id: str

    job_description_id: str

    category: str

    difficulty: str

    question_count: int = 5