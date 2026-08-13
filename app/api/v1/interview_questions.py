from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.dependencies.auth import (
    get_current_user,
)

from app.core.dependencies.database import (
    get_db,
)

from app.core.dependencies.services import (
    get_interview_question_service,
)

from app.models.user import User

from app.schemas.interview_question import (
    InterviewQuestionResponse,
)

from app.schemas.interview_question_generate import (
    InterviewQuestionGenerateRequest,
)

from app.schemas.regenerate_questions import (
    RegenerateQuestionsRequest,
)

from app.services.interview_question_service import (
    InterviewQuestionService,
)


router = APIRouter(
    prefix="/interview/questions",
    tags=["Interview Questions"],
)


@router.post(
    "/generate",
    response_model=list[
        InterviewQuestionResponse
    ],
    summary="Generate interview questions",
    description=(
        "Generate personalized interview "
        "questions using the user's resume "
        "and job description."
    ),
    response_description=(
        "Generated interview questions."
    ),
)
async def generate_questions(
    data: InterviewQuestionGenerateRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
     service: InterviewQuestionService = Depends(
        get_interview_question_service,
    ),
):

    return await service.generate_questions(
        db=db,
        user_id=str(current_user.id),
        resume_id=data.resume_id,
        job_description_id=(
            data.job_description_id
        ),
        category=data.category,
        difficulty=data.difficulty,
        question_count=data.question_count,
    )


@router.get(
    "/my-questions",
    response_model=list[
        InterviewQuestionResponse
    ],
    summary="Get my interview questions",
    description=(
        "Retrieve all interview questions "
        "generated for the authenticated user."
    ),
    response_description=(
        "List of the user's interview questions."
    ),
)
async def get_my_questions(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
     service: InterviewQuestionService = Depends(
        get_interview_question_service,
    ),
):

    return await service.get_my_questions(
        db,
        str(current_user.id),
    )


@router.get(
    "/{question_id}",
    response_model=InterviewQuestionResponse,
    summary="Get interview question",
    description=(
        "Retrieve a specific interview "
        "question belonging to the authenticated user."
    ),
    response_description=(
        "The requested interview question."
    ),
)
async def get_question(
    question_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewQuestionService = Depends(
        get_interview_question_service,
    ),
):

    return await service.get_question(
        db,
        str(question_id),
        str(current_user.id),
    )


@router.post(
    "/regenerate",
    response_model=list[
        InterviewQuestionResponse
    ],
    summary="Regenerate interview questions",
    description=(
        "Generate a new set of personalized "
        "interview questions for the selected "
        "resume and job description."
    ),
    response_description=(
        "Regenerated interview questions."
    ),
)
async def regenerate_questions(
    request: RegenerateQuestionsRequest,
    db: AsyncSession = Depends(
        get_db,
    ),
    current_user: User = Depends(
        get_current_user,
    ),
    service: InterviewQuestionService = Depends(
        get_interview_question_service,
    ),
):

    return await service.regenerate_questions(
        db=db,
        user_id=str(current_user.id),
        resume_id=request.resume_id,
        job_description_id=(
            request.job_description_id
        ),
        category=request.category,
        difficulty=request.difficulty,
        question_count=request.question_count,
    )