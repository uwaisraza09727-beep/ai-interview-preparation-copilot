import uuid

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database.base_model import BaseModel



class InterviewAnswer(BaseModel):

    __tablename__ = "interview_answers"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
    )

    interview_question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interview_questions.id"),
    )

    answer: Mapped[str] = mapped_column(
        Text,
    )

    score: Mapped[int] = mapped_column(
        Integer,
    )

    feedback: Mapped[str] = mapped_column(
        Text,
    )

    strengths: Mapped[str] = mapped_column(
        Text,
    )

    improvements: Mapped[str] = mapped_column(
        Text,
    )

    overall_result: Mapped[str] = mapped_column(
        String(30),
    )

    question = relationship(
        "InterviewQuestion",
    )