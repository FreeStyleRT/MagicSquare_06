"""E001~E006 error envelope constants — Boundary SSOT (R-U2)."""

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
