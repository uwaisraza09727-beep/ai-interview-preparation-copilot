from app.utils.parsers.docx_parser import (
    extract_docx_text,
)
from app.utils.parsers.pdf_parser import (
    extract_pdf_text,
)
from app.utils.parsers.constants import (
    COMMON_SECTION_HEADERS,
)

def extract_resume_text(
    file_path: str,
    extension: str,
) -> str:

    extension = extension.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    raise ValueError(
        "Unsupported file type."
    )
    
def extract_name(
    text: str,
) -> str | None:

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if len(line) > 60:
            continue

        lower = line.lower()

        if lower in COMMON_SECTION_HEADERS:
            continue

        if "@" in line:
            continue

        if any(char.isdigit() for char in line):
            continue

        return line

    return None    