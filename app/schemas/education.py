from pydantic import BaseModel


class Education(BaseModel):

    degree: str | None = None

    branch: str | None = None

    college: str | None = None

    year: str | None = None