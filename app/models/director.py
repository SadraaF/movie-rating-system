from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .movie import Movie  # Avoid circular import


class Director(Base):
    """SQLAlchemy model for directors."""
    __tablename__ = "directors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    birth_year: Mapped[int | None]
    description: Mapped[str | None] = mapped_column(String(512))

    # Relationship to Movie (One-to-Many)
    movies: Mapped[List["Movie"]] = relationship(
        back_populates="director", cascade="all, delete-orphan"
    )