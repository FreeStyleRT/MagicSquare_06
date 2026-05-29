"""Structured failure responses for Boundary/Control layers."""

from pydantic import BaseModel

from src.boundary.error_codes import (
    DUPLICATE_NON_ZERO_CODE,
    DUPLICATE_NON_ZERO_MESSAGE,
    INVALID_BLANK_COUNT_CODE,
    INVALID_BLANK_COUNT_MESSAGE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    INVALID_VALUE_RANGE_CODE,
    INVALID_VALUE_RANGE_MESSAGE,
    NO_VALID_SOLUTION_CODE,
    NO_VALID_SOLUTION_MESSAGE,
)

__all__ = [
    "DUPLICATE_NON_ZERO_CODE",
    "DUPLICATE_NON_ZERO_MESSAGE",
    "FailureResponse",
    "INVALID_BLANK_COUNT_CODE",
    "INVALID_BLANK_COUNT_MESSAGE",
    "INVALID_SIZE_CODE",
    "INVALID_SIZE_MESSAGE",
    "INVALID_VALUE_RANGE_CODE",
    "INVALID_VALUE_RANGE_MESSAGE",
    "NO_VALID_SOLUTION_CODE",
    "NO_VALID_SOLUTION_MESSAGE",
    "duplicate_non_zero_failure",
    "invalid_blank_count_failure",
    "invalid_size_failure",
    "invalid_value_range_failure",
    "no_valid_solution_failure",
]


class FailureResponse(BaseModel):
    """Standard failure payload (AC-FR01-01, PRD §8.1 INVALID_SIZE)."""

    code: str
    message: str


def invalid_size_failure() -> FailureResponse:
    """Return the INVALID_SIZE failure contract."""
    return FailureResponse(code=INVALID_SIZE_CODE, message=INVALID_SIZE_MESSAGE)


def invalid_blank_count_failure() -> FailureResponse:
    """Return the INVALID_BLANK_COUNT failure contract (PRD E002)."""
    return FailureResponse(
        code=INVALID_BLANK_COUNT_CODE,
        message=INVALID_BLANK_COUNT_MESSAGE,
    )


def invalid_value_range_failure() -> FailureResponse:
    """Return the INVALID_VALUE_RANGE failure contract (PRD E003)."""
    return FailureResponse(
        code=INVALID_VALUE_RANGE_CODE,
        message=INVALID_VALUE_RANGE_MESSAGE,
    )


def duplicate_non_zero_failure() -> FailureResponse:
    """Return the DUPLICATE_NON_ZERO failure contract (PRD E004)."""
    return FailureResponse(
        code=DUPLICATE_NON_ZERO_CODE,
        message=DUPLICATE_NON_ZERO_MESSAGE,
    )


def no_valid_solution_failure() -> FailureResponse:
    """Return the NO_VALID_SOLUTION failure contract (PRD E006)."""
    return FailureResponse(
        code=NO_VALID_SOLUTION_CODE,
        message=NO_VALID_SOLUTION_MESSAGE,
    )
