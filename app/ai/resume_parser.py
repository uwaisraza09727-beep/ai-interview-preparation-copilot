import re

from app.schemas.parsed_resume import ParsedResume
from app.utils.parsers.parser import extract_name
from app.utils.parsers.skills import extract_skills
from app.utils.parsers.certifations import extract_certifications
from app.utils.parsers.education import (
    extract_education,
)

from app.utils.parsers.experience import (
    extract_experience,
)

from app.utils.parsers.projects import (
    extract_projects,
)


class ResumeParser:

    def parse(
        self,
        text: str,
    ) -> ParsedResume:

        email = None
        phone = None

        email_match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )

        if email_match:
            email = email_match.group()

        phone_match = re.search(
            r"\+?\d[\d\s\-]{8,15}",
            text,
        )

        if phone_match:
            phone = phone_match.group()
        
        name = extract_name(text)
        
        return ParsedResume(
            name=extract_name(text),
            email=email,
            phone=phone,
            skills=extract_skills(text),
            education=extract_education(text),
            experience=extract_experience(text),
            projects=extract_projects(text),
            certifications=extract_certifications(text),
        )