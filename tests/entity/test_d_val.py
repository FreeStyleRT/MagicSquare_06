"""Track B — D-VAL-01~06 (FR-04 MagicSquareValidator)."""

from __future__ import annotations

import copy

from src.entity.services.magic_square_validator import (
    MagicSquareValidator,
    is_magic_square,
)
from tests.entity.conftest import GRID_G0


def _copy_grid(grid: list[list[int]]) -> list[list[int]]:
    return copy.deepcopy(grid)


class TestDVal01G0CompleteGridTrue:
    """D-VAL-01 — G0 complete magic square → True."""

    def test_d_val_01_is_magic_square_g0_true(self, grid_g0: list[list[int]]) -> None:
        # Given: G0 complete magic square
        # When: is_magic_square(matrix)
        result = is_magic_square(grid_g0)

        # Then: valid magic square
        assert result is True

    def test_validator_class_matches_function(self, grid_g0: list[list[int]]) -> None:
        validator = MagicSquareValidator()

        assert validator.validate(grid_g0) is is_magic_square(grid_g0)


class TestDVal02RowSumMismatchFalse:
    """D-VAL-02 — row sum mismatch → False."""

    def test_d_val_02_row_sum_mismatch_false(self, grid_g0: list[list[int]]) -> None:
        # Given: G0 copy with row-0 sum broken
        matrix = _copy_grid(grid_g0)
        matrix[0][0] = 1

        # When: is_magic_square(matrix)
        result = is_magic_square(matrix)

        # Then: invalid
        assert result is False


class TestDVal03ColSumMismatchFalse:
    """D-VAL-03 — column sum mismatch → False."""

    def test_d_val_03_col_sum_mismatch_false(self, grid_g0: list[list[int]]) -> None:
        # Given: G0 copy with column sum broken
        matrix = _copy_grid(grid_g0)
        matrix[3][0] = 5

        # When: is_magic_square(matrix)
        result = is_magic_square(matrix)

        # Then: invalid
        assert result is False


class TestDVal04DiagonalMismatchFalse:
    """D-VAL-04 — diagonal sum mismatch → False."""

    def test_d_val_04_diagonal_mismatch_false(self, grid_g0: list[list[int]]) -> None:
        # Given: G0 copy with main diagonal broken
        matrix = _copy_grid(grid_g0)
        matrix[1][1] = 12

        # When: is_magic_square(matrix)
        result = is_magic_square(matrix)

        # Then: invalid
        assert result is False


class TestDVal05DuplicateOrInvalidSetFalse:
    """D-VAL-05 — duplicate non-zero → False."""

    def test_d_val_05_duplicate_nonzero_false(self, grid_g0: list[list[int]]) -> None:
        # Given: G0 copy with non-zero duplicate
        matrix = _copy_grid(grid_g0)
        matrix[1][1] = 5

        # When: is_magic_square(matrix)
        result = is_magic_square(matrix)

        # Then: invalid
        assert result is False


class TestDVal06ZeroInFullGridFalse:
    """D-VAL-06 — zero in complete grid → False."""

    def test_d_val_06_zero_in_complete_grid_false(
        self,
        grid_g0: list[list[int]],
    ) -> None:
        # Given: G0 copy with 0 inserted
        matrix = _copy_grid(grid_g0)
        matrix[2][2] = 0

        # When: is_magic_square(matrix)
        result = is_magic_square(matrix)

        # Then: invalid
        assert result is False


class TestMagicSquareValidatorContract:
    """AC-FR04-01~04 — row, column, diagonal, and combined invariants."""

    def test_g0_passes_all_row_sums(self, grid_g0: list[list[int]]) -> None:
        assert all(sum(row) == 34 for row in grid_g0)

    def test_g0_passes_all_column_sums(self, grid_g0: list[list[int]]) -> None:
        for col in range(4):
            assert sum(grid_g0[row][col] for row in range(4)) == 34

    def test_g0_passes_both_diagonals(self, grid_g0: list[list[int]]) -> None:
        main_diag = sum(grid_g0[i][i] for i in range(4))
        anti_diag = sum(grid_g0[i][3 - i] for i in range(4))

        assert main_diag == 34
        assert anti_diag == 34

    def test_partial_grid_with_blanks_is_invalid(self) -> None:
        from tests.entity.conftest import GRID_G2

        assert is_magic_square(GRID_G2) is False
