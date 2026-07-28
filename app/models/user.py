from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base_model import BaseModel
from app.enums.user_role import UserRole
from sqlalchemy.orm import relationship
from app.models.job_description import JobDescription

class User(BaseModel):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    resumes = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    
    job_descriptions = relationship(
        "JobDescription",
        back_populates="user",
        cascade="all, delete-orphan",
    )