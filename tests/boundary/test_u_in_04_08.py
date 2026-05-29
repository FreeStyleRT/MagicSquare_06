"""Track A — U-IN-04~08: FR-01 blank count, value range, duplicate (AC-FR01-02~04)."""

from __future__ import annotations

import pytest

from src.boundary.validator import BoundaryValidator
from tests.conftest import (
    GRID_DUPLICATE_NON_ZERO,
    GRID_ONE_BLANK,
    GRID_THREE_BLANKS,
    GRID_VALUE_ABOVE_RANGE,
    GRID_VALUE_BELOW_RANGE,
    GRID_ZERO_BLANKS,
)
from tests.helpers.fr01_contract import (
    DUPLICATE_NON_ZERO_CODE,
    DUPLICATE_NON_ZERO_MESSAGE,
    INVALID_BLANK_COUNT_CODE,
    INVALID_BLANK_COUNT_MESSAGE,
    INVALID_VALUE_RANGE_CODE,
    INVALID_VALUE_RANGE_MESSAGE,
    FailureResponse,
)


class TestUIn04ZeroEmptyCellsReturnsE002:
    """U-IN-04 / AC-FR01-02 — blank count 0 → INVALID_BLANK_COUNT."""

    def test_u_in_04_zero_empty_cells_returns_e002(self) -> None:
        # Given: 4x4 grid with no blank cells (G0)
        validator = BoundaryValidator()
        matrix = GRID_ZERO_BLANKS

        # When: validate is invoked
        result = validator.validate(matrix)

        # Then: INVALID_BLANK_COUNT failure envelope
        assert result.code == INVALID_BLANK_COUNT_CODE
        assert result.message == INVALID_BLANK_COUNT_MESSAGE


class TestUIn05ThreeBlanksReturnsE002:
    """U-IN-05 / AC-FR01-02 — blank count 3 → INVALID_BLANK_COUNT."""

    def test_u_in_05_three_blanks_returns_e002(self) -> None:
        # Given: 4x4 grid with three zeros
        validator = BoundaryValidator()
        matrix = GRID_THREE_BLANKS

        # When: validate is invoked
        result = validator.validate(matrix)

        # Then: INVALID_BLANK_COUNT failure envelope
        assert result.code == INVALID_BLANK_COUNT_CODE
        assert result.message == INVALID_BLANK_COUNT_MESSAGE


class TestUIn05OneBlankReturnsE002:
    """AC-FR01-02 — blank count 1 → INVALID_BLANK_COUNT."""

    def test_u_in_05_one_blank_returns_e002(self) -> None:
        validator = BoundaryValidator()

        result = validator.validate(GRID_ONE_BLANK)

        assert result.code == INVALID_BLANK_COUNT_CODE
        assert result.message == INVALID_BLANK_COUNT_MESSAGE


class TestUIn06ValueBelowRangeReturnsE004:
    """U-IN-06 / AC-FR01-03 — value -1 → INVALID_VALUE_RANGE."""

    def test_u_in_06_value_below_range_returns_e004(self) -> None:
        # Given: valid 4x4 with -1 inserted
        validator = BoundaryValidator()
        matrix = GRID_VALUE_BELOW_RANGE

        # When: validate is invoked
        result = validator.validate(matrix)

        # Then: INVALID_VALUE_RANGE failure envelope
        assert result.code == INVALID_VALUE_RANGE_CODE
        assert result.message == INVALID_VALUE_RANGE_MESSAGE


class TestUIn07ValueAboveRangeReturnsE004:
    """U-IN-07 / AC-FR01-03 — value 17 → INVALID_VALUE_RANGE."""

    def test_u_in_07_value_above_range_returns_e004(self) -> None:
        # Given: valid 4x4 with 17 inserted
        validator = BoundaryValidator()
        matrix = GRID_VALUE_ABOVE_RANGE

        # When: validate is invoked
        result = validator.validate(matrix)

        # Then: INVALID_VALUE_RANGE failure envelope
        assert result.code == INVALID_VALUE_RANGE_CODE
        assert result.message == INVALID_VALUE_RANGE_MESSAGE


class TestUIn08DuplicateNonZeroReturnsE005:
    """U-IN-08 / AC-FR01-04 — duplicate non-zero → DUPLICATE_NON_ZERO."""

    def test_u_in_08_duplicate_nonzero_returns_e005(self) -> None:
        # Given: valid 4x4 with duplicate non-zero (second 2 in row 0)
        validator = BoundaryValidator()
        matrix = GRID_DUPLICATE_NON_ZERO

        # When: validate is invoked
        result = validator.validate(matrix)

        # Then: DUPLICATE_NON_ZERO failure envelope
        assert result.code == DUPLICATE_NON_ZERO_CODE
        assert result.message == DUPLICATE_NON_ZERO_MESSAGE


class TestFr01ExtendedNoExceptionPropagation:
    """EX-01 — FR-01-02~04 grids return FailureResponse without raising."""

    @pytest.mark.parametrize(
        ("grid", "expected_code"),
        [
            (GRID_ZERO_BLANKS, INVALID_BLANK_COUNT_CODE),
            (GRID_THREE_BLANKS, INVALID_BLANK_COUNT_CODE),
            (GRID_ONE_BLANK, INVALID_BLANK_COUNT_CODE),
            (GRID_VALUE_BELOW_RANGE, INVALID_VALUE_RANGE_CODE),
            (GRID_VALUE_ABOVE_RANGE, INVALID_VALUE_RANGE_CODE),
            (GRID_DUPLICATE_NON_ZERO, DUPLICATE_NON_ZERO_CODE),
        ],
        ids=[
            "zero_blanks",
            "three_blanks",
            "one_blank",
            "below_range",
            "above_range",
            "duplicate",
        ],
    )
    def test_extended_grids_never_raise(
        self,
        grid: list[list[int]],
        expected_code: str,
    ) -> None:
        validator = BoundaryValidator()

        result = validator.validate(grid)

        assert result.code == expected_code
        assert isinstance(result, FailureResponse)


class TestFr01ExtendedDeterminism:
    """EX-02 — identical invalid grid yields identical failure contract."""

    def test_same_blank_count_failure_is_deterministic(self) -> None:
        validator = BoundaryValidator()

        first = validator.validate(GRID_ZERO_BLANKS)
        second = validator.validate(GRID_ZERO_BLANKS)

        assert first.code == second.code == INVALID_BLANK_COUNT_CODE
        assert first.message == second.message == INVALID_BLANK_COUNT_MESSAGE


class TestFr01ValidationPriority:
    """Size check precedes content rules (AC-FR01-01 first)."""

    def test_invalid_size_precedes_blank_count(self) -> None:
        validator = BoundaryValidator()
        grid_3x4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

        result = validator.validate(grid_3x4)

        assert result.code == "INVALID_SIZE"
