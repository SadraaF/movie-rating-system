from sqlalchemy.ext.asyncio import AsyncSession
from app.models.movie_rating import MovieRating

class RatingRepository:
    """Repository for managing MovieRating data."""

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository.
        :param session: The database session.
        """
        self._session = session

    async def create(self, rating: MovieRating) -> MovieRating:
        """
        Save a new rating to the database.
        :param rating: The rating instance to save.
        :return: The saved rating instance.
        """
        self._session.add(rating)
        await self._session.commit()
        await self._session.refresh(rating)
        return rating