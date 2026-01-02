from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .director import Director
    from .genre import Genre
    from .movie_rating import MovieRating


# Association Table for Movie-Genre Many-to-Many relationship
movie_genres_association = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


class Movie(Base):
    """SQLAlchemy model for movies."""
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    release_year: Mapped[int]
    cast: Mapped[str | None] = mapped_column(String(512))
    description: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    # Foreign Key to directors table
    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id"))

    # Relationship to Director (Many-to-One)
    director: Mapped["Director"] = relationship(back_populates="movies")

    # Relationship to MovieRating (One-to-Many)
    ratings: Mapped[List["MovieRating"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )

    # Relationship to Genre (Many-to-Many)
    genres: Mapped[List["Genre"]] = relationship(
        secondary=movie_genres_association, back_populates="movies"
    )