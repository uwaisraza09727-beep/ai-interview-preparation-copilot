import uuid

from sqlalchemy import Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base_model import BaseModel




class MatchResult(BaseModel):
    __tablename__ = "match_results"

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

    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    matched_skills: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
    )

    missing_skills: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
    )

    matched_keywords: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
    )

    missing_keywords: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="match_results",
    )

    resume = relationship(
        "Resume",
    )

    job_description = relationship(
        "JobDescription",
    )