import re

from app.utils.parsers.skills import extract_skills


class ResumeMatcher:

    def calculate_match(
        self,
        resume_text: str,
        jd_text: str,
    ) -> dict:

        # Extract skills
        resume_skills = extract_skills(
            resume_text,
        )

        jd_skills = extract_skills(
            jd_text,
        )

        matched_skills = sorted(
            set(resume_skills) & set(jd_skills)
        )

        missing_skills = sorted(
            set(jd_skills) - set(resume_skills)
        )

        # Extract all words
        resume_words = set(
            re.findall(
                r"\w+",
                resume_text.lower(),
            )
        )

        jd_words = set(
            re.findall(
                r"\w+",
                jd_text.lower(),
            )
        )

        matched_keywords = sorted(
            resume_words & jd_words
        )

        missing_keywords = sorted(
            jd_words - resume_words
        )

        # Calculate score
        score = 0

        if jd_skills:
            score = round(
                len(matched_skills)
                / len(jd_skills)
                * 100,
                2,
            )

        return {
            "overall_score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
        }