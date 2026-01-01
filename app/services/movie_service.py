from typing import Sequence, Any
from app.repositories.movie_repository import MovieRepository
from app.exceptions.repository_exceptions import EntityNotFoundError

class MovieService:
    """Service layer for Movie-related business logic."""

    def __init__(self, movie_repo: MovieRepository):
        """
        Initialize the service.
        :param movie_repo: Injected MovieRepository instance.
        """
        self._movie_repo = movie_repo

    async def list_movies(
        self, 
        page: int, 
        page_size: int,
        title: str | None = None,
        year: int | None = None,
        genre: str | None = None
    ) -> dict[str, Any]:
        """
        Orchestrate the retrieval of a paginated movie list.
        """
        skip = (page - 1) * page_size
        movies, total = await self._movie_repo.get_all_paginated(
            skip, page_size, title, year, genre
        )

        items = []
        for m in movies:
            avg, count = await self._movie_repo.get_avg_rating(m.id)
            items.append({
                "id": m.id,
                "title": m.title,
                "release_year": m.release_year,
                "director": {"id": m.director.id, "name": m.director.name},
                "genres": [g.name for g in m.genres],
                "average_rating": avg
            })

        return {
            "page": page,
            "page_size": page_size,
            "total_items": total,
            "items": items
        }

    async def get_movie_details(self, movie_id: int) -> dict[str, Any]:
        """
        Retrieve full details for a movie, including aggregated ratings.
        :raises EntityNotFoundError: If movie doesn't exist.
        """
        movie = await self._movie_repo.get_by_id(movie_id)
        if not movie:
            raise EntityNotFoundError("Movie", movie_id)

        avg, count = await self._movie_repo.get_avg_rating(movie_id)
        
        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": {
                "id": movie.director.id,
                "name": movie.director.name,
                "birth_year": movie.director.birth_year,
                "description": movie.director.description
            },
            "genres": [g.name for g in movie.genres],
            "cast": movie.cast,
            "average_rating": avg,
            "ratings_count": count
        }