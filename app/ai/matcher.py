import re

from app.utils.parsers.skills import extract_skills


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
    "you",
    "your",
    "we",
    "will",
}


class ResumeMatcher:

    def calculate_match(
        self,
        resume_text: str,
        jd_text: str,
    ) -> dict:

        resume_skills = extract_skills(
            resume_text,
        )

        jd_skills = extract_skills(
            jd_text,
        )

        matched_skills = sorted(
            set(resume_skills)
            & set(jd_skills)
        )

        missing_skills = sorted(
            set(jd_skills)
            - set(resume_skills)
        )

        resume_words = set(
            re.findall(
                r"\b[a-zA-Z0-9+#.-]+\b",
                resume_text.lower(),
            )
        )

        jd_words = set(
            re.findall(
                r"\b[a-zA-Z0-9+#.-]+\b",
                jd_text.lower(),
            )
        )

        resume_keywords = (
            resume_words - STOP_WORDS
        )

        jd_keywords = (
            jd_words - STOP_WORDS
        )

        matched_keywords = sorted(
            resume_keywords
            & jd_keywords
        )

        missing_keywords = sorted(
            jd_keywords
            - resume_keywords
        )

        skill_score = 0.0

        if jd_skills:
            skill_score = (
                len(matched_skills)
                / len(jd_skills)
            ) * 100

        keyword_score = 0.0

        if jd_keywords:
            keyword_score = (
                len(matched_keywords)
                / len(jd_keywords)
            ) * 100

        overall_score = round(
            (skill_score * 0.70)
            + (keyword_score * 0.30),
            2,
        )

        return {
            "overall_score": overall_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
        }