from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/db")
async def test_database(db: AsyncSession = Depends(get_db)):
    return {
        "message": "Database dependency injected successfully!"
    }