class KemonoError(Exception):
    """Project-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class KemonoValidationError(KemonoError):
    """Validation errors."""
