import re

SKILLS = [
    "python",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "git",
    "github",
    "linux",
    "aws",
    "azure",
    "gcp",
    "tensorflow",
    "pytorch",
    "opencv",
    "numpy",
    "pandas",
    "machine learning",
    "deep learning",
    "langchain",
    "rag",
    "openai",
    "llm",
]

def extract_skills(
    text: str,
) -> list[str]:

    text = text.lower()

    found = []

    for skill in SKILLS:

        if re.search(
            rf"\b{re.escape(skill)}\b",
            text,
        ):
            found.append(skill)

    return sorted(set(found))