from pydantic import BaseModel, Field

class MovieCreateRequest(BaseModel):
    """Schema for creating a new movie."""
    title: str = Field(..., min_length=1, max_length=255)
    director_id: int
    release_year: int = Field(..., gt=1880, lt=2100)
    cast: str | None = Field(None, max_length=512)
    genres: list[int]

class MovieUpdateRequest(BaseModel):
    """Schema for updating an existing movie."""
    title: str | None = Field(None, min_length=1, max_length=255)
    release_year: int | None = Field(None, gt=1880, lt=2100)
    cast: str | None = Field(None, max_length=512)
    genres: list[int] | None = None

class RatingCreateRequest(BaseModel):
    """Schema for registering a rating."""
    score: int = Field(...)