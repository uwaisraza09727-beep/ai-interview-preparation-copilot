from app.services.interview_answer_service import (
    InterviewAnswerService,
)

from app.services.interview_question_service import (
    InterviewQuestionService,
)

from app.services.interview_session_service import (
    InterviewSessionService,
)


def get_interview_answer_service(
) -> InterviewAnswerService:

    return InterviewAnswerService()


def get_interview_question_service(
) -> InterviewQuestionService:

    return InterviewQuestionService()


def get_interview_session_service(
) -> InterviewSessionService:

    return InterviewSessionService()