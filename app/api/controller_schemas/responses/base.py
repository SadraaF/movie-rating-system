from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response format."""
    status: str = "success"
    data: T

class FailureResponse(BaseModel):
    """Standard failure response format."""
    status: str = "failure"
    error: dict[str, Any]