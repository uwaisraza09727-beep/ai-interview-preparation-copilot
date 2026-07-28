import re

from app.schemas.education import Education
from app.utils.parsers.section_parser import extract_section


def extract_education(
    text: str,
) -> list[Education]:

    lines = extract_section(
        text,
        "education",
    )
    
    

    degree = None
    branch = None
    college = None
    year = None

    for line in lines:

        lower = line.lower()

        if (
            "b.tech" in lower
            or "btech" in lower
            or "m.tech" in lower
            or "mtech" in lower
            or "b.e" in lower
            or "computer science" in lower
        ):
            degree = line

        elif (
            "college" in lower
            or "university" in lower
            or "institute" in lower
            or "aktu" in lower
        ):
            college = line

        match = re.search(
            r"\b(19|20)\d{2}\s*[-–]\s*(19|20)?\d{2}\b",
            line,
        )

        if match:
            year = match.group()

    return [
        Education(
            degree=degree,
            branch=branch,
            college=college,
            year=year,
        )
    ]