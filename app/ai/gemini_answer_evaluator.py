from google import genai

from app.core.config.settings import settings

from app.schemas.answer_feedback import (
    AnswerFeedback,
)


class GeminiAnswerEvaluator:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    async def evaluate_answer(
        self,
        question: str,
        user_answer: str,
    ) -> AnswerFeedback:

        prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer.

Interview Question:

{question}

Candidate Answer:

{user_answer}

Evaluate the answer honestly.

Scoring Rules:

- Score should be between 0 and 100.
- Consider correctness.
- Consider completeness.
- Consider communication.
- Consider practical understanding.

Return JSON only.

overall_result must be one of:

Excellent
Good
Average
Poor

feedback should be short.

strengths should mention the strongest point.

improvements should mention how to improve.
"""

        response = await self.client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": (
                    AnswerFeedback.model_json_schema()
                ),
            },
        )

        return AnswerFeedback.model_validate_json(
            response.text
        )