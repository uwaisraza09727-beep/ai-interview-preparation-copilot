from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.database import get_db

from app.models.user import User

from app.schemas.match import MatchResponse

from app.services.matching_service import MatchingService


router = APIRouter(
    prefix="/matching",
    tags=["Matching"],
)

matching_service = MatchingService()


@router.post(
    "/{resume_id}/{job_description_id}",
    response_model=MatchResponse,
)
async def match_resume_with_job_description(
    resume_id: str,
    job_description_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await matching_service.match_resume_with_jd(
            db=db,
            resume_id=resume_id,
            job_description_id=job_description_id,
            user_id=str(current_user.id),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )