"""Boundary refactor Wave 4 — error codes and result formatter SSOT (R-U2, R-U3)."""

from __future__ import annotations

from src.boundary.contracts import (
    duplicate_non_zero_failure,
    invalid_blank_count_failure,
    invalid_size_failure,
    invalid_value_range_failure,
    no_valid_solution_failure,
)
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
from src.boundary.result_formatter import SOLUTION_LENGTH, ResultFormatter


class TestErrorCodesSsot:
    """R-U2 — factories delegate to error_codes SSOT."""

    def test_invalid_size_factory_uses_error_codes(self) -> None:
        failure = invalid_size_failure()

        assert failure.code == INVALID_SIZE_CODE
        assert failure.message == INVALID_SIZE_MESSAGE

    def test_invalid_blank_count_factory_uses_error_codes(self) -> None:
        failure = invalid_blank_count_failure()

        assert failure.code == INVALID_BLANK_COUNT_CODE
        assert failure.message == INVALID_BLANK_COUNT_MESSAGE

    def test_invalid_value_range_factory_uses_error_codes(self) -> None:
        failure = invalid_value_range_failure()

        assert failure.code == INVALID_VALUE_RANGE_CODE
        assert failure.message == INVALID_VALUE_RANGE_MESSAGE

    def test_duplicate_non_zero_factory_uses_error_codes(self) -> None:
        failure = duplicate_non_zero_failure()

        assert failure.code == DUPLICATE_NON_ZERO_CODE
        assert failure.message == DUPLICATE_NON_ZERO_MESSAGE

    def test_no_valid_solution_factory_uses_error_codes(self) -> None:
        failure = no_valid_solution_failure()

        assert failure.code == NO_VALID_SOLUTION_CODE
        assert failure.message == NO_VALID_SOLUTION_MESSAGE


class TestResultFormatterSsot:
    """R-U3 — E007 int[6] / 1-index validation at Boundary."""

    def test_solution_length_constant(self) -> None:
        assert SOLUTION_LENGTH == 6

    def test_format_builds_six_element_vector(self) -> None:
        result = ResultFormatter.format(1, 1, 16, 4, 4, 1)

        assert result == [1, 1, 16, 4, 4, 1]

    def test_is_valid_solution_format_accepts_g2_vector(self) -> None:
        assert ResultFormatter.is_valid_solution_format([3, 3, 6, 4, 4, 1])

    def test_is_valid_solution_format_rejects_zero_index(self) -> None:
        assert ResultFormatter.is_valid_solution_format([0, 1, 2, 3, 4, 5]) is False

    def test_is_valid_solution_format_rejects_wrong_length(self) -> None:
        assert ResultFormatter.is_valid_solution_format([1, 2, 3]) is False
