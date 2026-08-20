from abc import ABC, abstractmethod

from app.schemas.answer_feedback import AnswerFeedback


class AnswerEvaluator(ABC):

    @abstractmethod
    async def evaluate_answer(
        self,
        question: str,
        user_answer: str,
    ) -> AnswerFeedback:
        pass