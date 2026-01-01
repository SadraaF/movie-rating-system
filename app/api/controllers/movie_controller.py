from fastapi import APIRouter, Depends, Query, status, Response

from app.api.dependencies import get_movie_service, get_rating_service
from app.services.movie_service import MovieService
from app.services.rating_service import RatingService
from app.api.controller_schemas.requests.movie import (
    MovieCreateRequest, MovieUpdateRequest, RatingCreateRequest
)
from app.api.controller_schemas.responses.base import SuccessResponse
from app.api.controller_schemas.responses.movie import (
    MoviePaginatedResponse, MovieDetailResponse, RatingResponse
)

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("", response_model=SuccessResponse[MoviePaginatedResponse])
async def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    title: str | None = None,
    release_year: int | None = None,
    genre: str | None = None,
    service: MovieService = Depends(get_movie_service)
):
    """Retrieve a paginated and filtered list of movies."""
    data = await service.list_movies(page, page_size, title, release_year, genre)
    return SuccessResponse(data=data)

@router.get("/{movie_id}", response_model=SuccessResponse[MovieDetailResponse])
async def get_movie(
    movie_id: int, 
    service: MovieService = Depends(get_movie_service)
):
    """Retrieve details for a specific movie."""
    data = await service.get_movie_details(movie_id)
    return SuccessResponse(data=data)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse[MovieDetailResponse])
async def add_movie(
    request: MovieCreateRequest, 
    service: MovieService = Depends(get_movie_service)
):
    """Register a new movie."""
    data = await service.add_movie(request.dict())
    return SuccessResponse(data=data)

@router.put("/{movie_id}", response_model=SuccessResponse[MovieDetailResponse])
async def update_movie(
    movie_id: int, 
    request: MovieUpdateRequest, 
    service: MovieService = Depends(get_movie_service)
):
    """Update movie information."""
    data = await service.update_movie(movie_id, request.dict(exclude_unset=True))
    return SuccessResponse(data=data)

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: int, 
    service: MovieService = Depends(get_movie_service)
):
    """Remove a movie from the system."""
    await service.delete_movie(movie_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{movie_id}/ratings", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse[RatingResponse])
async def rate_movie(
    movie_id: int,
    request: RatingCreateRequest,
    service: RatingService = Depends(get_rating_service)
):
    """Register a rating for a specific movie."""
    data = await service.add_rating(movie_id, request.score)
    return SuccessResponse(data=data)