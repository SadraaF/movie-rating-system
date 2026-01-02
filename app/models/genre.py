from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, func
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

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    # Relationship to Movie (Many-to-Many)
    movies: Mapped[List["Movie"]] = relationship(
        secondary="movie_genres", back_populates="genres"
    )