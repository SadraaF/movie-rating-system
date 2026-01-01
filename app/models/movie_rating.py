from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .movie import Movie


class MovieRating(Base):
    """SQLAlchemy model for movie ratings."""
    __tablename__ = "movie_ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    score: Mapped[int]
    rated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationship to Movie (Many-to-One)
    movie: Mapped["Movie"] = relationship(back_populates="ratings")