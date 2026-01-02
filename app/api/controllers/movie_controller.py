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
    """
    Retrieve a paginated and filtered list of movies.
    :param page: The page number to retrieve.
    :param page_size: Number of items per page.
    :param title: Optional title filter (partial match).
    :param release_year: Optional release year filter.
    :param genre: Optional genre name filter.
    :param service: The injected MovieService.
    :return: A success response containing the paginated data.
    """
    data = await service.list_movies(page, page_size, title, release_year, genre)
    return SuccessResponse(data=data)

@router.get("/{movie_id}", response_model=SuccessResponse[MovieDetailResponse])
async def get_movie(
    movie_id: int, 
    service: MovieService = Depends(get_movie_service)
):
    """
    Retrieve full details for a specific movie.
    :param movie_id: The unique ID of the movie.
    :param service: Injected MovieService.
    :return: Success response with movie details.
    :raises EntityNotFoundError: If the movie does not exist.
    """
    data = await service.get_movie_details(movie_id)
    return SuccessResponse(data=data)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse[MovieDetailResponse])
async def add_movie(
    request: MovieCreateRequest, 
    service: MovieService = Depends(get_movie_service)
):
    """
    Register a new movie in the system and establish its relationships.
    :param request: The pydantic schema containing movie details and associated IDs.
    :param service: The injected MovieService instance.
    :return: A success response containing the created movie's full details.
    :raises ValidationError: If the director_id or one of the genre_ids is invalid.
    """
    data = await service.add_movie(request.dict())
    return SuccessResponse(data=data)

@router.put("/{movie_id}", response_model=SuccessResponse[MovieDetailResponse])
async def update_movie(
    movie_id: int, 
    request: MovieUpdateRequest, 
    service: MovieService = Depends(get_movie_service)
):
    """
    Update an existing movie's information and synchronize its genre relationships.
    :param movie_id: The unique identifier of the movie to update.
    :param request: The pydantic schema containing partial or full fields to update.
    :param service: The injected MovieService instance.
    :return: A success response containing the updated movie's full details.
    :raises EntityNotFoundError: If no movie matches the provided movie_id.
    :raises ValidationError: If provided genre IDs are invalid.
    """
    data = await service.update_movie(movie_id, request.dict(exclude_unset=True))
    return SuccessResponse(data=data)

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: int, 
    service: MovieService = Depends(get_movie_service)
):
    """
    Remove a movie and its associated ratings from the system.
    :param movie_id: The unique ID of the movie to delete.
    :param service: Injected MovieService.
    :return: Empty response with 204 status.
    :raises EntityNotFoundError: If the movie does not exist.
    """
    await service.delete_movie(movie_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{movie_id}/ratings", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse[RatingResponse])
async def rate_movie(
    movie_id: int,
    request: RatingCreateRequest,
    service: RatingService = Depends(get_rating_service)
):
    """
    Register a rating for a specific movie.
    :param movie_id: The ID of the movie to rate.
    :param request: The rating request body (score).
    :param service: The injected RatingService.
    :return: The created rating details.
    :raises AppError: If movie is not found or validation fails.
    """
    data = await service.add_rating(movie_id, request.score)
    return SuccessResponse(data=data)