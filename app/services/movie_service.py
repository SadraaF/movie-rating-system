import logging
from typing import Any

from app.core.decorators import log_execution_time
from app.repositories.movie_repository import MovieRepository
from app.repositories.director_repository import DirectorRepository
from app.repositories.genre_repository import GenreRepository
from app.exceptions.repository_exceptions import EntityNotFoundError
from app.exceptions.service_exceptions import ValidationError
from app.models.movie import Movie

logger = logging.getLogger("app.movie_service")

class MovieService:
    """Service layer for Movie-related business logic."""

    def __init__(
        self, 
        movie_repo: MovieRepository,
        director_repo: DirectorRepository,
        genre_repo: GenreRepository
    ):
        """
        Initialize the service with necessary repositories.
        :param movie_repo: Injected MovieRepository.
        :param director_repo: Injected DirectorRepository.
        :param genre_repo: Injected GenreRepository.
        """
        self._movie_repo = movie_repo
        self._director_repo = director_repo
        self._genre_repo = genre_repo

    @log_execution_time
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
        logger.info(f"Fetching movie list: page={page}, size={page_size}, filters={{'title': {title}, 'year': {year}, 'genre': {genre}}}")

        skip = (page - 1) * page_size
        results, total = await self._movie_repo.get_all_paginated(
            skip, page_size, title, year, genre
        )

        items = []
        for row in results:
            movie, avg_rating, count = row
            
            final_avg = round(float(avg_rating), 1) if avg_rating else None

            items.append({
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "director": {"id": movie.director.id, "name": movie.director.name},
                "genres": [g.name for g in movie.genres],
                "average_rating": final_avg,
                "ratings_count": count
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

    async def add_movie(self, movie_data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new movie after validating director and genres.
        :param movie_data: Dictionary containing title, director_id, year, cast, genres.
        :return: Created movie details.
        :raises ValidationError: If director or genres are invalid.
        """
        # Validate Director
        director = await self._director_repo.get_by_id(movie_data["director_id"])
        if not director:
            raise ValidationError(f"Director with ID {movie_data['director_id']} does not exist.")

        # Validate Genres
        genres = await self._genre_repo.get_by_ids(movie_data["genres"])
        if len(genres) != len(movie_data["genres"]):
            raise ValidationError("One or more provided genre IDs are invalid.")

        new_movie = Movie(
            title=movie_data["title"],
            director_id=movie_data["director_id"],
            release_year=movie_data["release_year"],
            cast=movie_data.get("cast"),
            genres=list(genres)
        )
        
        created = await self._movie_repo.create(new_movie)
        return await self.get_movie_details(created.id)

    async def update_movie(self, movie_id: int, update_data: dict[str, Any]) -> dict[str, Any]:
        """
        Update an existing movie and sync its genres.
        :param movie_id: ID of the movie to update.
        :param update_data: Data to update.
        :return: Updated movie details.
        :raises EntityNotFoundError: If movie doesn't exist.
        """
        movie = await self._movie_repo.get_by_id(movie_id)
        if not movie:
            raise EntityNotFoundError("Movie", movie_id)

        # Update basic fields
        if "title" in update_data: movie.title = update_data["title"]
        if "release_year" in update_data: movie.release_year = update_data["release_year"]
        if "cast" in update_data: movie.cast = update_data["cast"]

        # Sync Genres if provided
        if "genres" in update_data:
            genres = await self._genre_repo.get_by_ids(update_data["genres"])
            if len(genres) != len(update_data["genres"]):
                raise ValidationError("One or more provided genre IDs are invalid.")
            movie.genres = list(genres)

        await self._movie_repo.update()
        return await self.get_movie_details(movie.id)

    async def delete_movie(self, movie_id: int) -> None:
        """
        Delete a movie. Cascade delete is handled by DB/ORM.
        :param movie_id: ID of the movie to delete.
        :raises EntityNotFoundError: If movie doesn't exist.
        """
        movie = await self._movie_repo.get_by_id(movie_id)
        if not movie:
            raise EntityNotFoundError("Movie", movie_id)
        
        await self._movie_repo.delete(movie)