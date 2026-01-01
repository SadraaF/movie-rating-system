from sqlalchemy.orm import DeclarativeBase

from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie, movie_genres_association
from app.models.movie_rating import MovieRating

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass