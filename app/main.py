from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.resume import router as resume_router
from app.api.v1.matching import router as matching_router

from app.api.v1.job_description import (
    router as job_description_router,
)

app = FastAPI(
    title="AI Interview Preparation Copilot",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(resume_router)
app.include_router(job_description_router)
app.include_router(
    matching_router,
)


@app.get("/")
async def root():
    return {
        "message": "AI Interview Preparation Copilot API"
    }