from pydantic import BaseModel, Field


class JobDescriptionTextCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    jd_text: str = Field(
        min_length=20,
    )