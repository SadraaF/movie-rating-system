from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.director import Director

class DirectorRepository:
    """Repository for managing Director data."""

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository.
        :param session: The database session.
        """
        self._session = session

    async def get_by_id(self, director_id: int) -> Director | None:
        """
        Retrieve a director by ID.
        :param director_id: The ID of the director.
        :return: Director object or None.
        """
        result = await self._session.execute(
            select(Director).where(Director.id == director_id)
        )
        return result.scalar_one_or_none()