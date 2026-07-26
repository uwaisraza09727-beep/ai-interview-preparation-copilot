from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    UploadFile,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.database import get_db

from app.models.user import User

from app.schemas.resume import ResumeResponse

from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

resume_service = ResumeService()


@router.post(
    "/upload",
    response_model=ResumeResponse,
)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await resume_service.upload_resume(
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
    "/my-resumes",
    response_model=list[ResumeResponse],
)
async def get_my_resumes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    return await resume_service.get_my_resumes(
        db,
        str(current_user.id),
    )   
    
@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:
        return await resume_service.get_resume(
            db,
            resume_id,
            str(current_user.id),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
        
@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:
        await resume_service.delete_resume(
            db,
            resume_id,
            str(current_user.id),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )             