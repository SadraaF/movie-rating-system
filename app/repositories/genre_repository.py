from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from app.models.genre import Genre

class GenreRepository:
    """Repository for managing Genre data."""

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository.
        :param session: The database session.
        """
        self._session = session

    async def get_by_ids(self, genre_ids: list[int]) -> Sequence[Genre]:
        """
        Retrieve multiple genres by a list of IDs.
        :param genre_ids: List of integer IDs.
        :return: A sequence of Genre objects.
        """
        result = await self._session.execute(
            select(Genre).where(Genre.id.in_(genre_ids))
        )
        return result.scalars().all()