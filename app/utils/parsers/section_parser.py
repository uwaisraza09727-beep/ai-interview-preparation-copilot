SECTION_HEADERS = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "about",
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
    ],

    "projects": [
        "projects",
        "project",
    ],

    "experience": [
        "experience",
        "work experience",
        "employment",
    ],

    "education": [
        "education",
        "academic",
        "qualification",
    ],

    "certifications": [
        "certifications",
        "certification",
        "licenses",
    ],
}


def extract_section(
    text: str,
    section_name: str,
) -> list[str]:

    headers = SECTION_HEADERS.get(
        section_name,
        [],
    )

    lines = text.splitlines()

    collecting = False

    result = []

    all_headers = [
        h.lower()
        for values in SECTION_HEADERS.values()
        for h in values
    ]

    for line in lines:

        current = line.strip()

        lower = (
            current.lower()
            .replace(":", "")
            .strip()
        )
        
        if lower in headers:
            collecting = True
            continue

        if collecting and lower in all_headers:
            break

        if collecting and current.strip():
            result.append(current)

    return result