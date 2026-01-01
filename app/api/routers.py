from fastapi import APIRouter
from app.api.controllers import movie_controller

api_router = APIRouter()

# Include the movie routes under the /api/v1 prefix
api_router.include_router(movie_controller.router, prefix="/api/v1")