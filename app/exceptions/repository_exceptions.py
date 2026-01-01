from .base import AppError

class RepositoryError(AppError):
    """Base class for database layer errors."""
    pass

class EntityNotFoundError(RepositoryError):
    """Raised when a requested record does not exist."""
    def __init__(self, entity_name: str, entity_id: int | str):
        super().__init__(f"{entity_name} with ID {entity_id} not found", code=404)