from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, func
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

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    # Relationship to Movie (One-to-Many)
    movies: Mapped[List["Movie"]] = relationship(
        back_populates="director", cascade="all, delete-orphan"
    )