"""Magic square validation for completed candidate grids (FR-04)."""

from __future__ import annotations

from src.entity.constants import (
    BLANK_CELL_VALUE,
    CELL_MAX_VALUE,
    CELL_MIN_VALUE,
    GRID_DIMENSION,
    MATRIX_SIZE,
)
from src.entity.services.grid_sums import (
    is_magic_sum,
    sum_anti_diagonal,
    sum_col,
    sum_main_diagonal,
    sum_row,
)


class MagicSquareValidator:
    """Validates row, column, diagonal sums and 1..16 set completeness."""

    def validate(self, grid: list[list[int]]) -> bool:
        """Return True when the grid satisfies all magic-square invariants.

        Args:
            grid: Completed 4x4 candidate matrix (no blanks).

        Returns:
            True when row, column, diagonal sums and value set are valid.
        """
        if not self._has_complete_value_set(grid):
            return False
        if not self._all_row_sums_valid(grid):
            return False
        if not self._all_col_sums_valid(grid):
            return False
        return self._both_diagonals_valid(grid)

    def _has_complete_value_set(self, grid: list[list[int]]) -> bool:
        values = [cell for row in grid for cell in row]
        if BLANK_CELL_VALUE in values:
            return False
        if len(values) != MATRIX_SIZE * MATRIX_SIZE:
            return False
        if len(set(values)) != len(values):
            return False
        return all(CELL_MIN_VALUE <= value <= CELL_MAX_VALUE for value in values)

    def _all_row_sums_valid(self, grid: list[list[int]]) -> bool:
        return all(is_magic_sum(sum_row(grid, row)) for row in range(GRID_DIMENSION))

    def _all_col_sums_valid(self, grid: list[list[int]]) -> bool:
        return all(
            is_magic_sum(sum_col(grid, col)) for col in range(GRID_DIMENSION)
        )

    def _both_diagonals_valid(self, grid: list[list[int]]) -> bool:
        return is_magic_sum(sum_main_diagonal(grid)) and is_magic_sum(
            sum_anti_diagonal(grid),
        )


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return True when grid satisfies magic-square invariants (FR-04).

    Args:
        grid: Completed 4x4 candidate matrix.

    Returns:
        True when all FR-04 conditions pass.
    """
    return MagicSquareValidator().validate(grid)
