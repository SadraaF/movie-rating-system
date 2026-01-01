from datetime import datetime
from typing import Any
from app.repositories.rating_repository import RatingRepository
from app.repositories.movie_repository import MovieRepository
from app.exceptions.repository_exceptions import EntityNotFoundError
from app.exceptions.service_exceptions import ValidationError
from app.models.movie_rating import MovieRating

class RatingService:
    """Service layer for Movie Ratings."""

    def __init__(self, rating_repo: RatingRepository, movie_repo: MovieRepository):
        """
        Initialize the service.
        :param rating_repo: Injected RatingRepository.
        :param movie_repo: Injected MovieRepository.
        """
        self._rating_repo = rating_repo
        self._movie_repo = movie_repo

    async def add_rating(self, movie_id: int, score: int) -> dict[str, Any]:
        """
        Add a rating to a movie.
        :param movie_id: ID of the movie.
        :param score: Integer between 1 and 10.
        :return: Created rating details.
        :raises EntityNotFoundError: If movie doesn't exist.
        :raises ValidationError: If score is out of range.
        """
        if not (1 <= score <= 10):
            raise ValidationError("Score must be an integer between 1 and 10")

        movie = await self._movie_repo.get_by_id(movie_id)
        if not movie:
            raise EntityNotFoundError("Movie", movie_id)

        new_rating = MovieRating(
            movie_id=movie_id,
            score=score,
            rated_at=datetime.utcnow()
        )
        
        created = await self._rating_repo.create(new_rating)
        
        return {
            "rating_id": created.id,
            "movie_id": created.movie_id,
            "score": created.score,
            "created_at": created.rated_at.isoformat()
        }