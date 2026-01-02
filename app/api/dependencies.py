"""
FastAPI dependencies for database sessions and service injection.
Handles the lifecycle of SQLAlchemy async sessions.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.session import AsyncSessionLocal
from app.repositories.movie_repository import MovieRepository
from app.repositories.director_repository import DirectorRepository
from app.repositories.genre_repository import GenreRepository
from app.repositories.rating_repository import RatingRepository
from app.services.movie_service import MovieService
from app.services.rating_service import RatingService

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide a database session."""
    async with AsyncSessionLocal() as session:
        yield session

def get_movie_service(db: AsyncSession = Depends(get_db)) -> MovieService:
    """Dependency to provide a MovieService instance."""
    return MovieService(
        movie_repo=MovieRepository(db),
        director_repo=DirectorRepository(db),
        genre_repo=GenreRepository(db)
    )

def get_rating_service(db: AsyncSession = Depends(get_db)) -> RatingService:
    """Dependency to provide a RatingService instance."""
    return RatingService(
        rating_repo=RatingRepository(db),
        movie_repo=MovieRepository(db)
    )