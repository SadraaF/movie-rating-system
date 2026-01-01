from .base import AppError

class ServiceError(AppError):
    """Base class for business logic errors."""
    pass

class ValidationError(ServiceError):
    """Raised when data validation fails."""
    def __init__(self, message: str):
        super().__init__(message, code=422)