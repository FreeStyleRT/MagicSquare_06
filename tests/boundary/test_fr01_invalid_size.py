"""AC-FR01-01, PRD §8.1 INVALID_SIZE — matrix size validation (Boundary only)."""

from __future__ import annotations

from typing import Any

import pytest

from magic_square.boundary.validator import BoundaryValidator
from tests.conftest import AC_FR01_01_INVALID_SIZE_GRIDS, OUT_OF_SCOPE_VALID_4X4
from tests.helpers.fr01_contract import (
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    FailureResponse,
)


class TestInvalidSizeFailureReturn:
    """AC-FR01-01, PRD §8.1 INVALID_SIZE — happy path of failure (None input)."""

    def test_none_grid_returns_invalid_size_failure(
        self,
        grid_none: None,
        expected_invalid_size_dict: dict[str, str],
    ) -> None:
        # AC-FR01-01
        # Given: explicit None grid (not a 4x4 matrix)
        validator = BoundaryValidator()

        # When: validate is invoked
        result = validator.validate(grid_none)

        # Then: structured failure with INVALID_SIZE contract
        assert result.code == expected_invalid_size_dict["code"]
        assert result.message == expected_invalid_size_dict["message"]


class TestInvalidSizeBoundaryValues:
    """AC-FR01-01, PRD §8.1 INVALID_SIZE — size mismatch boundary grids."""

    @pytest.mark.parametrize(
        ("grid_key", "grid"),
        [
            ("empty", []),
            ("four_rows_zero_columns", [[]] * 4),
            (
                "three_by_four",
                [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
            ),
            (
                "four_by_three",
                [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
            ),
            (
                "five_by_five",
                [[1, 2, 3, 4, 5] for _ in range(5)],
            ),
        ],
        ids=[
            "empty_list",
            "four_rows_zero_cols",
            "three_by_four",
            "four_by_three",
            "five_by_five",
        ],
    )
    def test_invalid_size_grid_returns_failure(
        self,
        grid_key: str,
        grid: list[list[int]],
    ) -> None:
        # AC-FR01-01
        # Given: a grid that violates 4x4 dimensions
        validator = BoundaryValidator()

        # When: validate is invoked
        result = validator.validate(grid)

        # Then: INVALID_SIZE failure is returned
        assert result.code == INVALID_SIZE_CODE
        assert result.message == INVALID_SIZE_MESSAGE


class TestInvalidSizeMessageContract:
    """AC-FR01-01, PRD §8.1 INVALID_SIZE — message character-level equality."""

    def test_none_grid_message_matches_prd_invalid_size_exactly(
        self,
        grid_none: None,
    ) -> None:
        # AC-FR01-01
        # Given: None grid and PRD §8.1 INVALID_SIZE message contract
        validator = BoundaryValidator()
        expected_message = "Grid must be 4x4."

        # When: validate is invoked
        result = validator.validate(grid_none)

        # Then: message matches exactly (character-level)
        assert result.message == expected_message
        assert len(result.message) == len(expected_message)


class TestInvalidSizeFailureCodeContract:
    """AC-FR01-01, PRD §8.1 INVALID_SIZE — failure code exact match."""

    def test_none_grid_code_is_invalid_size_literal(self, grid_none: None) -> None:
        # AC-FR01-01
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate is invoked
        result = validator.validate(grid_none)

        # Then: code is exactly INVALID_SIZE
        assert result.code == "INVALID_SIZE"
        assert result.code == INVALID_SIZE_CODE


class TestInvalidSizeResponseType:
    """AC-FR01-01, PRD §8.1 INVALID_SIZE — failure result structure."""

    def test_none_grid_returns_failure_response_model(
        self,
        grid_none: None,
    ) -> None:
        # AC-FR01-01
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate is invoked
        result = validator.validate(grid_none)

        # Then: result is the designated FailureResponse structure
        parsed = FailureResponse.model_validate(result)
        assert parsed.code == INVALID_SIZE_CODE
        assert parsed.message == INVALID_SIZE_MESSAGE


class TestInvalidSizeScopeLimit:
    """AC-FR01-01 scope guard — excludes AC-FR01-02~05 and FR-02~05 cases."""

    def test_scope_excludes_valid_4x4_and_downstream_domain_cases(self) -> None:
        # AC-FR01-01
        # Given: module-scoped invalid-size grid registry for this RED commit
        registered_grids: list[Any] = list(AC_FR01_01_INVALID_SIZE_GRIDS.values())

        # When: comparing against out-of-scope valid 4x4 fixture
        # Then: valid 4x4 is not part of AC-FR01-01 RED inputs
        assert OUT_OF_SCOPE_VALID_4X4 not in registered_grids
        assert len(registered_grids) == 6
        assert all(
            key
            in {
                "none",
                "empty",
                "four_rows_zero_columns",
                "three_by_four",
                "four_by_three",
                "five_by_five",
            }
            for key in AC_FR01_01_INVALID_SIZE_GRIDS
        )


class TestInvalidSizeNoExceptionPropagation:
    """EX-01 — BV-01~06 each returns FailureResponse without raising."""

    @pytest.mark.parametrize(
        ("grid_key", "grid"),
        list(AC_FR01_01_INVALID_SIZE_GRIDS.items()),
        ids=list(AC_FR01_01_INVALID_SIZE_GRIDS.keys()),
    )
    def test_boundary_values_never_raise(
        self,
        grid_key: str,
        grid: Any,
    ) -> None:
        # EX-01
        validator = BoundaryValidator()

        result = validator.validate(grid)

        assert result.code == INVALID_SIZE_CODE
        assert result.message == INVALID_SIZE_MESSAGE


class TestInvalidSizeDeterminism:
    """EX-02 — identical invalid grid yields identical failure contract."""

    def test_same_invalid_grid_returns_identical_failure_twice(self) -> None:
        # EX-02
        grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
        validator = BoundaryValidator()

        first = validator.validate(grid)
        second = validator.validate(grid)

        assert first.code == second.code == INVALID_SIZE_CODE
        assert first.message == second.message == INVALID_SIZE_MESSAGE


class TestInvalidSizeNonListDefensive:
    """EX-03 — non-list grid types return INVALID_SIZE defensively."""

    @pytest.mark.parametrize(
        "grid",
        ["invalid", 4, {}],
        ids=["string", "int", "dict"],
    )
    def test_non_list_grid_returns_invalid_size(self, grid: Any) -> None:
        # EX-03
        validator = BoundaryValidator()

        result = validator.validate(grid)

        assert result.code == INVALID_SIZE_CODE
        assert result.message == INVALID_SIZE_MESSAGE


class TestInvalidSizeUnevenRowLengths:
    """EX-04 — per-row column length check rejects uneven rows."""

    def test_uneven_row_lengths_returns_invalid_size(self) -> None:
        # EX-04
        grid = [[1, 2, 3, 4], [1, 2], [1, 2, 3, 4], [1, 2, 3, 4]]
        validator = BoundaryValidator()

        result = validator.validate(grid)

        assert result.code == INVALID_SIZE_CODE
        assert result.message == INVALID_SIZE_MESSAGE


class TestInvalidSizeNoneRowElement:
    """EX-05 — None row element fails isinstance(row, list) check."""

    def test_none_row_element_returns_invalid_size(self) -> None:
        # EX-05
        grid: list[Any] = [[1, 2, 3, 4], None, [1, 2, 3, 4], [1, 2, 3, 4]]
        validator = BoundaryValidator()

        result = validator.validate(grid)

        assert result.code == INVALID_SIZE_CODE
        assert result.message == INVALID_SIZE_MESSAGE


class TestInvalidSizeInputImmutability:
    """EX-06 — validate does not mutate the caller's grid."""

    def test_validate_does_not_mutate_input_grid(self) -> None:
        # EX-06
        grid = [[1, 2, 3, 4], [1, 2], [1, 2, 3, 4], [1, 2, 3, 4]]
        expected = [[1, 2, 3, 4], [1, 2], [1, 2, 3, 4], [1, 2, 3, 4]]
        validator = BoundaryValidator()

        validator.validate(grid)

        assert grid == expected
