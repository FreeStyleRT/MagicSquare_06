"""Structured failure responses for Boundary/Control layers."""

from pydantic import BaseModel

INVALID_SIZE_CODE: str = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."


class FailureResponse(BaseModel):
    """Standard failure payload (AC-FR01-01, PRD §8.1 INVALID_SIZE)."""

    code: str
    message: str


def invalid_size_failure() -> FailureResponse:
    """Return the INVALID_SIZE failure contract."""
    return FailureResponse(code=INVALID_SIZE_CODE, message=INVALID_SIZE_MESSAGE)
