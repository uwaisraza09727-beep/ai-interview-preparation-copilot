from pydantic import BaseModel


class ParsedResume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    skills: list[str] = []

    education: list[str] = []

    experience: list[str] = []

    projects: list[str] = []

    certifications: list[str] = []