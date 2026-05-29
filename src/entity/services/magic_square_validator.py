"""Magic square validation for completed candidate grids (FR-04)."""

from __future__ import annotations

from src.entity.constants import (
    BLANK_CELL_VALUE,
    CELL_MAX_VALUE,
    CELL_MIN_VALUE,
    GRID_DIMENSION,
    MAGIC_SUM,
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
        if len(values) != GRID_DIMENSION * GRID_DIMENSION:
            return False
        if len(set(values)) != len(values):
            return False
        return all(CELL_MIN_VALUE <= value <= CELL_MAX_VALUE for value in values)

    def _all_row_sums_valid(self, grid: list[list[int]]) -> bool:
        return all(sum(row) == MAGIC_SUM for row in grid)

    def _all_col_sums_valid(self, grid: list[list[int]]) -> bool:
        for col in range(GRID_DIMENSION):
            if sum(grid[row][col] for row in range(GRID_DIMENSION)) != MAGIC_SUM:
                return False
        return True

    def _both_diagonals_valid(self, grid: list[list[int]]) -> bool:
        main_diag = sum(grid[i][i] for i in range(GRID_DIMENSION))
        anti_diag = sum(
            grid[i][GRID_DIMENSION - 1 - i] for i in range(GRID_DIMENSION)
        )
        return main_diag == MAGIC_SUM and anti_diag == MAGIC_SUM


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return True when grid satisfies magic-square invariants (FR-04).

    Args:
        grid: Completed 4x4 candidate matrix.

    Returns:
        True when all FR-04 conditions pass.
    """
    return MagicSquareValidator().validate(grid)
