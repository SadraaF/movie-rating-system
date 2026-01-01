class AppError(Exception):
    """Base class for all application-specific exceptions."""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)