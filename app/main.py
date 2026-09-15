from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.resume import router as resume_router
from app.api.v1.matching import router as matching_router
from app.api.v1.dashboard import router as dashboard_router

from app.api.v1.job_description import (
    router as job_description_router,
)

from app.api.v1.interview_questions import (
    router as interview_questions_router,
)

from app.api.v1.interview_answers import (
    router as interview_answer_router,
)

from app.core.exceptions import (
    register_exception_handlers,
)

from app.api.v1.interview_sessions import (
    router as interview_session_router,
)


app = FastAPI(
    title="AI Interview Preparation Copilot",
    summary="AI-powered interview preparation and evaluation platform",
    description=(
        "Backend API for resume analysis, "
        "job description matching, "
        "interview question generation, "
        "answer evaluation, "
        "and interview session management."
    ),
    version="1.0.0",
)


# CORS configuration for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_exception_handlers(app)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(resume_router)
app.include_router(job_description_router)
app.include_router(matching_router)
app.include_router(dashboard_router)
app.include_router(interview_questions_router)
app.include_router(interview_answer_router)
app.include_router(interview_session_router)


@app.get("/")
async def root():
    return {
        "message": "AI Interview Preparation Copilot API"
    }