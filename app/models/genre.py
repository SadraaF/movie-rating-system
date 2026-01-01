from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .movie import Movie  # Avoid circular import


class Genre(Base):
    """SQLAlchemy model for genres."""
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(512))

    # Relationship to Movie (Many-to-Many)
    movies: Mapped[List["Movie"]] = relationship(
        secondary="movie_genres", back_populates="genres"
    )