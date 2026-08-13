import uuid

from sqlalchemy import ForeignKey, String, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base_model import BaseModel


class InterviewQuestion(BaseModel):
    __tablename__ = "interview_questions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    resume_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
    )

    job_description_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job_descriptions.id"),
        nullable=False,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    difficulty: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    user = relationship(
        "User",
    )

    resume = relationship(
        "Resume",
    )

    job_description = relationship(
        "JobDescription",
    )
    
    difficulty: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    question_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )