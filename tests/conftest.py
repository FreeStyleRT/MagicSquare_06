"""Shared pytest fixtures for Magic Square RED tests."""

from __future__ import annotations

from typing import Any

import pytest

from tests.helpers.fr01_contract import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


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
}

# Explicitly out of scope for this RED commit (AC-FR01-02~05, FR-02~05).
OUT_OF_SCOPE_VALID_4X4: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]
