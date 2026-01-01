import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.api.routers import api_router
from app.exceptions.base import AppError
from app.logging_config import setup_logging

setup_logging()

if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="Movie Rating System API",
    description="A back-end system for managing movies, directors, and ratings.",
    version="1.0.0"
)

# Register the main router
app.include_router(api_router)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """
    Global handler for custom application errors.
    Converts AppError to the standardized failure response format.
    """
    return JSONResponse(
        status_code=exc.code,
        content={
            "status": "failure",
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Overrides the default FastAPI validation error to match project standards.
    """
    return JSONResponse(
        status_code=422,
        content={
            "status": "failure",
            "error": {
                "code": 422,
                "message": str(exc.errors())
            }
        }
    )

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint to verify API health."""
    return {"message": "Movie Rating System API is running"}