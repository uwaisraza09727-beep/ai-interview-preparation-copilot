from fastapi import FastAPI

from app.api.test import router as test_router

app = FastAPI(
    title="AI Interview Preparation Copilot",
    version="1.0.0",
    description="Backend API for AI Interview Preparation Copilot",
)

app.include_router(test_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Interview Preparation Copilot API"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }