"""Shared pytest fixtures for Magic Square RED tests."""

from __future__ import annotations

from typing import Any

import pytest

from tests.helpers.fr01_contract import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register Golden Master approve flag."""
    parser.addoption(
        "--golden-approve",
        action="store_true",
        default=False,
        help="Overwrite tests/golden_master_expected.txt with current output",
    )


@pytest.fixture
def golden_approve(request: pytest.FixtureRequest) -> bool:
    """Return True when --golden-approve is passed on the CLI."""
    return bool(request.config.getoption("--golden-approve"))


@pytest.fixture
def grid_none() -> None:
    return None


@pytest.fixture
def grid_empty() -> list[list[int]]:
    return []


@pytest.fixture
def grid_four_rows_zero_columns() -> list[list[int]]:
    return [[]] * 4


@pytest.fixture
def grid_3x4() -> list[list[int]]:
    return [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]


@pytest.fixture
def expected_invalid_size_dict() -> dict[str, str]:
    return {"code": INVALID_SIZE_CODE, "message": INVALID_SIZE_MESSAGE}


# AC-FR01-01 only: size-invalid inputs (no valid 4x4, no FR-01-02~05 cases).
AC_FR01_01_INVALID_SIZE_GRIDS: dict[str, Any] = {
    "none": None,
    "empty": [],
    "four_rows_zero_columns": [[]] * 4,
    "three_by_four": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
    "four_by_three": [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
    "five_by_five": [[1, 2, 3, 4, 5] for _ in range(5)],
}

# Explicitly out of scope for this RED commit (AC-FR01-02~05, FR-02~05).
OUT_OF_SCOPE_VALID_4X4: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# AC-FR01-02~04: valid 4x4 shape, invalid FR-01 content rules.
GRID_ZERO_BLANKS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

GRID_THREE_BLANKS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 0, 0],
]

GRID_ONE_BLANK: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

GRID_VALUE_BELOW_RANGE: list[list[int]] = [
    [-1, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

GRID_VALUE_ABOVE_RANGE: list[list[int]] = [
    [17, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

GRID_DUPLICATE_NON_ZERO: list[list[int]] = [
    [16, 2, 2, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]
