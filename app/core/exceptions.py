from fastapi import (
    FastAPI,
    Request,
)

from fastapi.responses import JSONResponse


class AIServiceError(
    Exception,
):
    pass


def register_exception_handlers(
    app: FastAPI,
):

    @app.exception_handler(
        ValueError
    )
    async def value_error_handler(
        request: Request,
        exc: ValueError,
    ):

        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(
        AIServiceError
    )
    async def ai_service_error_handler(
        request: Request,
        exc: AIServiceError,
    ):

        return JSONResponse(
            status_code=503,
            content={
                "detail": str(exc),
            },
        )