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
    get_interview_answer_service,
)


from app.models.user import User

from app.schemas.common import (
    MessageResponse,
)

from app.schemas.interview_answer import (
    InterviewAnswerPerformanceResponse,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
)

from app.services.interview_answer_service import (
    InterviewAnswerService,
)


router = APIRouter(
    prefix="/interview/answers",
    tags=["Interview Answers"],
)


@router.post(
    "/evaluate",
    response_model=InterviewAnswerResponse,
    summary="Evaluate interview answer",
    description=(
        "Evaluate the authenticated user's "
        "answer to an interview question using AI."
    ),
    response_description=(
        "AI evaluation of the interview answer."
    ),
)
async def evaluate_answer(
    request: InterviewAnswerRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewAnswerService = Depends(
        get_interview_answer_service,
    ),
):

    return await service.evaluate_answer(
        db=db,
        user_id=str(current_user.id),
        interview_question_id=(
            request.interview_question_id
        ),
        answer=request.answer,
    )


@router.get(
    "/my",
    response_model=list[
        InterviewAnswerResponse
    ],
    summary="Get my interview answers",
    description=(
        "Retrieve all interview answers "
        "submitted by the authenticated user."
    ),
    response_description=(
        "List of the user's interview answers."
    ),
)
async def get_my_answers(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewAnswerService = Depends(
        get_interview_answer_service,
    ),
):

    return await service.get_my_answers(
        db,
        str(current_user.id),
    )


@router.get(
    "/performance",
    response_model=(
        InterviewAnswerPerformanceResponse
    ),
    summary="Get interview performance",
    description=(
        "Retrieve interview performance "
        "statistics for the authenticated user."
    ),
    response_description=(
        "Interview performance statistics."
    ),
)
async def get_performance(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewAnswerService = Depends(
        get_interview_answer_service,
    ),
):

    return await service.get_performance(
        db,
        str(current_user.id),
    )


@router.get(
    "/{answer_id}",
    response_model=InterviewAnswerResponse,
    summary="Get interview answer",
    description=(
        "Retrieve a specific interview answer "
        "belonging to the authenticated user."
    ),
    response_description=(
        "The requested interview answer."
    ),
)
async def get_answer(
    answer_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewAnswerService = Depends(
        get_interview_answer_service,
    ),
):

    return await service.get_answer(
        db,
        str(answer_id),
        str(current_user.id),
    )


@router.delete(
    "/{answer_id}",
    response_model=MessageResponse,
    summary="Delete interview answer",
    description=(
        "Delete an interview answer belonging "
        "to the authenticated user."
    ),
    response_description=(
        "Confirmation that the answer was deleted."
    ),
)
async def delete_answer(
    answer_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewAnswerService = Depends(
        get_interview_answer_service,
    ),
):

    await service.delete_answer(
        db,
        str(answer_id),
        str(current_user.id),
    )

    return MessageResponse(
        message="Answer deleted successfully"
    )