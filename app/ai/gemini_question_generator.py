from google import genai

from app.core.config.settings import settings
from app.schemas.generated_question import (
    GeneratedQuestions,
)


class GeminiQuestionGenerator:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    async def generate_questions(
        self,
        resume_text: str,
        jd_text: str,
        category: str,
        difficulty: str,
        question_count: int,
        existing_questions: list[str],
    ) -> GeneratedQuestions:

        prompt = f"""
You are an expert technical interviewer.

Generate exactly {question_count}
interview questions based on the candidate's
resume and the job description.

Category requested:
{category}

Difficulty requested:
{difficulty}

Candidate Resume:
{resume_text}

Job Description:
{jd_text}

Existing Questions:
{chr(10).join(existing_questions)}

Requirements:

- Questions must be directly relevant to the resume.
- Questions must be relevant to the job description.
- Avoid duplicate questions.
- Focus on practical interview questions.
- Questions should test the candidate's actual skills
  and project experience.
- Generate exactly {question_count} questions.

Never generate any question that already exists
in Existing Questions.

Return only completely new questions.

For each question, classify question_type as one
of these values:

technical
project
behavioral
situational
conceptual
"""

        response = await self.client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": (
                    GeneratedQuestions.model_json_schema()
                ),
            },
        )

        return GeneratedQuestions.model_validate_json(
            response.text
        )