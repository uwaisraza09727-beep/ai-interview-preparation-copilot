import uuid

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.database.base_model import BaseModel


class Resume(BaseModel):
    __tablename__ = "resumes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    upload_status: Mapped[str] = mapped_column(
        String(30),
        default="uploaded",
        nullable=False,
    )
    
    resume_text: Mapped[str | None] = mapped_column(
    nullable=True,
    )

    user = relationship(
        "User",
        back_populates="resumes",
    )