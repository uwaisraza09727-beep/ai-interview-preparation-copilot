from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.auth import (
    get_current_user,
)

from app.core.dependencies.database import (
    get_db,
)

from app.core.dependencies.services import (
    get_interview_session_service,
)

from app.models.user import User

from app.schemas.interview_session import (
    StartInterviewRequest,
    InterviewSessionResponse,
)

from app.services.interview_session_service import (
    InterviewSessionService,
)

from app.schemas.interview_question import (
    InterviewQuestionResponse,
)

from app.schemas.interview_dashboard import (
    InterviewDashboardResponse,
)

from app.schemas.interview_summary import (
    InterviewSummaryResponse,
)


router = APIRouter(
    prefix="/interview/session",
    tags=["Interview Session"],
)


@router.post(
    "/start",
    response_model=InterviewSessionResponse,
    summary="Start an interview session",
    description=(
        "Starts a new interview session for the "
        "authenticated user using the selected "
        "resume and job description."
    ),
    responses={
        400: {
            "description": (
                "An interview session is already active "
                "or interview questions have not been generated."
            ),
        },
    },
)
async def start_session(
    request: StartInterviewRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewSessionService = Depends(
        get_interview_session_service,
    ),
):

    return await service.start_session(
        db=db,
        user_id=str(current_user.id),
        resume_id=request.resume_id,
        job_description_id=request.job_description_id,
    )


@router.get(
    "/active",
    response_model=InterviewSessionResponse,
    summary="Get active interview session",
    description=(
        "Returns the currently active interview "
        "session for the authenticated user."
    ),
    responses={
        400: {
            "description": (
                "No active interview session exists."
            ),
        },
    },
)
async def get_active_session(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewSessionService = Depends(
        get_interview_session_service,
    ),
):

    return await service.get_active_session(
        db,
        str(current_user.id),
    )


@router.post(
    "/finish",
    response_model=InterviewSessionResponse,
    summary="Finish interview session",
    description=(
        "Marks the currently active interview "
        "session as completed."
    ),
    responses={
        400: {
            "description": (
                "No active interview session exists."
            ),
        },
    },
)
async def finish_session(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewSessionService = Depends(
        get_interview_session_service,
    ),
):

    return await service.finish_session(
        db,
        str(current_user.id),
    )


@router.get(
    "/current-question",
    response_model=InterviewQuestionResponse,
    summary="Get current interview question",
    description=(
        "Returns the next unanswered question "
        "for the active interview session."
    ),
    responses={
        400: {
            "description": (
                "No active interview session or "
                "current question is available."
            ),
        },
    },
)
async def get_current_question(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewSessionService = Depends(
        get_interview_session_service,
    ),
):

    return await service.get_current_question(
        db,
        str(current_user.id),
    )


@router.get(
    "/dashboard",
    response_model=InterviewDashboardResponse,
    summary="Get interview dashboard",
    description=(
        "Returns interview progress including "
        "total, answered and remaining questions."
    ),
    responses={
        400: {
            "description": (
                "No active interview session exists."
            ),
        },
    },
)
async def dashboard(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewSessionService = Depends(
        get_interview_session_service,
    ),
):

    return await service.get_dashboard(
        db,
        str(current_user.id),
    )


@router.get(
    "/summary",
    response_model=InterviewSummaryResponse,
    summary="Get interview summary",
    description=(
        "Returns overall interview statistics "
        "for the authenticated user."
    ),
    responses={
        400: {
            "description": (
                "Interview summary cannot be generated."
            ),
        },
    },
)
async def get_summary(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewSessionService = Depends(
        get_interview_session_service,
    ),
):

    return await service.get_summary(
        db,
        str(current_user.id),
    )


@router.get(
    "/recent",
    response_model=list[
        InterviewSessionResponse
    ],
    summary="Get recent interview sessions",
    description=(
        "Returns the most recent interview "
        "sessions for the authenticated user."
    ),
)
async def get_recent_sessions(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
    service: InterviewSessionService = Depends(
        get_interview_session_service,
    ),
):

    return await service.get_recent_sessions(
        db,
        str(current_user.id),
    )