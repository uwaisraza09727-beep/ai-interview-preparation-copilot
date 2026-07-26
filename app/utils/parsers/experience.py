from app.utils.parsers.section_parser import extract_section


def extract_experience(
    text: str,
) -> list[str]:

    return extract_section(
        text,
        "experience",
    )