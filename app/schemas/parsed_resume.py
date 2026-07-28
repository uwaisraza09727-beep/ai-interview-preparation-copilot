from pydantic import BaseModel
from app.schemas.education import Education


class ParsedResume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    skills: list[str] = []

    education: list[Education] = []
    
    experience: list[str] = []

    projects: list[str] = []

    certifications: list[str] = []