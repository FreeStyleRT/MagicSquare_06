"""Structured failure responses for Boundary/Control layers."""

from pydantic import BaseModel

INVALID_SIZE_CODE: str = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."

INVALID_BLANK_COUNT_CODE: str = "INVALID_BLANK_COUNT"
INVALID_BLANK_COUNT_MESSAGE: str = (
    "Exactly two blank cells (`0`) are required."
)

INVALID_VALUE_RANGE_CODE: str = "INVALID_VALUE_RANGE"
INVALID_VALUE_RANGE_MESSAGE: str = "Values must be `0` or `1..16`."

DUPLICATE_NON_ZERO_CODE: str = "DUPLICATE_NON_ZERO"
DUPLICATE_NON_ZERO_MESSAGE: str = "Duplicate non-zero values are not allowed."

NO_VALID_SOLUTION_CODE: str = "NO_VALID_SOLUTION"
NO_VALID_SOLUTION_MESSAGE: str = (
    "No valid magic square result for both attempts."
)


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
