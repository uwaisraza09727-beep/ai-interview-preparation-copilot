class QuestionGenerator:

    async def generate_questions(
        self,
        resume_text: str,
        jd_text: str,
        category: str,
        difficulty: str,
        question_count: int,
    ) -> list[str]:

        raise NotImplementedError