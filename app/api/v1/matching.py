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

from app.schemas.match_result import MatchResultResponse

from app.services.matching_service import MatchingService


router = APIRouter(
    prefix="/matching",
    tags=["Matching"],
)

matching_service = MatchingService()


@router.post(
    "/{resume_id}/{job_description_id}",
    response_model=MatchResultResponse,
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
        
@router.get(
    "/history",
    response_model=list[MatchResultResponse],
)
async def get_match_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    return await matching_service.get_match_history(
        db,
        str(current_user.id),
    )
    
@router.get(
    "/history/{match_result_id}",
    response_model=MatchResultResponse,
)
async def get_match(
    match_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await matching_service.get_match(
            db,
            match_result_id,
            str(current_user.id),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )  
          
@router.delete(
    "/{match_result_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_match(
    match_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:

        await matching_service.delete_match(
            db,
            match_result_id,
            str(current_user.id),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )    