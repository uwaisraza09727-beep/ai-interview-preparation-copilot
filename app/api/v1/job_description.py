from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.database import get_db

from app.models.user import User

from app.schemas.job_description import (
    JobDescriptionResponse,
)

from app.services.job_description_service import (
    JobDescriptionService,
)
from app.schemas.job_description_text import (
    JobDescriptionTextCreate,
)


router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"],
)

job_description_service = JobDescriptionService()


@router.post(
    "/upload",
    response_model=JobDescriptionResponse,
)
async def upload_job_description(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:
        return await job_description_service.upload_job_description(
            db,
            str(current_user.id),
            file,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/my-job-descriptions",
    response_model=list[JobDescriptionResponse],
)
async def get_my_job_descriptions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    return await job_description_service.get_my_job_descriptions(
        db,
        str(current_user.id),
    )


@router.get(
    "/{job_description_id}",
    response_model=JobDescriptionResponse,
)
async def get_job_description(
    job_description_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:
        return await job_description_service.get_job_description(
            db,
            job_description_id,
            str(current_user.id),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{job_description_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_job_description(
    job_description_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:
        await job_description_service.delete_job_description(
            db,
            job_description_id,
            str(current_user.id),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
        
@router.post(
    "/text",
    response_model=JobDescriptionResponse,
)
async def create_job_description_from_text(
    data: JobDescriptionTextCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await job_description_service.create_from_text(
            db=db,
            user_id=str(current_user.id),
            title=data.title,
            jd_text=data.jd_text,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )        