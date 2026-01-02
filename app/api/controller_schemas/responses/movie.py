from pydantic import BaseModel

class DirectorMinimal(BaseModel):
    id: int
    name: str

class DirectorDetailed(DirectorMinimal):
    birth_year: int | None
    description: str | None

class MovieBrief(BaseModel):
    id: int
    title: str
    release_year: int
    director: DirectorMinimal
    genres: list[str]
    average_rating: float | None
    ratings_count: int = 0

class MoviePaginatedResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    items: list[MovieBrief]

class MovieDetailResponse(MovieBrief):
    director: DirectorDetailed
    cast: str | None

class RatingResponse(BaseModel):
    rating_id: int
    movie_id: int
    score: int
    created_at: str