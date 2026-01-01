from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Sequence

from app.models.movie import Movie
from app.models.movie_rating import MovieRating
from app.models.genre import Genre

class MovieRepository:
    """Repository for managing Movie data in the database."""

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository.
        :param session: The database session to use for operations.
        """
        self._session = session

    async def get_all_paginated(
        self, 
        skip: int = 0, 
        limit: int = 10,
        title: str | None = None,
        release_year: int | None = None,
        genre_name: str | None = None
    ) -> tuple[Sequence[Movie], int]:
        """
        Retrieve a paginated list of movies with optional filtering.
        :param skip: Number of records to skip.
        :param limit: Maximum number of records to return.
        :param title: Partial title filter.
        :param release_year: Exact release year filter.
        :param genre_name: Exact genre name filter.
        :return: A tuple containing (list of movies, total count).
        """
        # Build the base query
        query = select(Movie).options(
            selectinload(Movie.director),
            selectinload(Movie.genres)
        )

        # Apply filters
        filters = []
        if title:
            filters.append(Movie.title.ilike(f"%{title}%"))
        if release_year:
            filters.append(Movie.release_year == release_year)
        if genre_name:
            query = query.join(Movie.genres).where(Genre.name == genre_name)

        if filters:
            query = query.where(and_(*filters))

        # Get total count before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_count = (await self._session.execute(count_query)).scalar_one()

        # Apply pagination and ordering
        query = query.offset(skip).limit(limit).order_by(Movie.id.desc())
        
        result = await self._session.execute(query)
        return result.scalars().all(), total_count

    async def get_by_id(self, movie_id: int) -> Movie | None:
        """
        Retrieve a single movie by its ID.
        :param movie_id: The ID of the movie.
        :return: Movie object or None.
        """
        query = select(Movie).where(Movie.id == movie_id).options(
            selectinload(Movie.director),
            selectinload(Movie.genres),
            selectinload(Movie.ratings)
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_avg_rating(self, movie_id: int) -> tuple[float | None, int]:
        """
        Calculate average rating and count for a movie.
        :param movie_id: The movie ID.
        :return: Tuple of (average_score, total_votes).
        """
        query = select(
            func.avg(MovieRating.score),
            func.count(MovieRating.id)
        ).where(MovieRating.movie_id == movie_id)
        
        result = await self._session.execute(query)
        avg, count = result.one()
        return (round(float(avg), 1) if avg else None, count)

    async def delete(self, movie: Movie) -> None:
        """
        Delete a movie record.
        :param movie: The movie instance to delete.
        """
        await self._session.delete(movie)
        await self._session.commit()

    async def create(self, movie: Movie) -> Movie:
        """
        Save a new movie to the database.
        :param movie: The movie instance to save.
        :return: The saved movie instance with its ID populated.
        """
        self._session.add(movie)
        await self._session.commit()
        await self._session.refresh(movie)
        return movie

    async def update(self) -> None:
        """
        Commit the current session changes to update a movie.
        """
        await self._session.commit()