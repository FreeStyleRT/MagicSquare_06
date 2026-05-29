"""Domain-layer exceptions for magic-square resolution."""


class UnsolvableDomainError(Exception):
    """Raised when both solver attempts fail to produce a valid magic square."""

    def __init__(self, message: str = "No valid magic square for both attempts.") -> None:
        super().__init__(message)
