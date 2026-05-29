"""Input matrix validation at the Boundary layer (FR-01)."""

from __future__ import annotations

from typing import Any

from src.boundary.constants import (
    CELL_MAX_VALUE,
    CELL_MIN_VALUE,
    GRID_DIMENSION,
    REQUIRED_BLANK_COUNT,
)
from src.boundary.contracts import (
    FailureResponse,
    duplicate_non_zero_failure,
    invalid_blank_count_failure,
    invalid_size_failure,
    invalid_value_range_failure,
)


class BoundaryValidator:
    """Validates FR-01 input contract before Domain entry."""

    def validate(self, grid: Any) -> FailureResponse | None:
        """Validate grid against FR-01 rules; return first failure encountered.

        Args:
            grid: Candidate input matrix.

        Returns:
            FailureResponse when any FR-01 contract is violated, else None
            when all FR-01 checks pass.
        """
        return self.validation_failure(grid)

    def validation_failure(self, grid: Any) -> FailureResponse | None:
        """Return the first FR-01 failure, or None when all checks pass.

        Args:
            grid: Candidate input matrix.

        Returns:
            FailureResponse on first violated contract, else None.
        """
        if self.is_size_invalid(grid):
            return invalid_size_failure()
        if self.is_blank_count_invalid(grid):
            return invalid_blank_count_failure()
        if self.is_value_range_invalid(grid):
            return invalid_value_range_failure()
        if self.is_duplicate_non_zero_invalid(grid):
            return duplicate_non_zero_failure()
        return None

    def is_input_invalid(self, grid: Any) -> bool:
        """Return True when any FR-01 validation rule is violated."""
        return self.validation_failure(grid) is not None

    def is_size_invalid(self, grid: Any) -> bool:
        """Return True when grid is not a 4x4 matrix (AC-FR01-01)."""
        return self._is_invalid_size(grid)

    def is_blank_count_invalid(self, grid: Any) -> bool:
        """Return True when zero count is not exactly 2 (AC-FR01-02)."""
        if self.is_size_invalid(grid):
            return False
        return self._count_blanks(grid) != REQUIRED_BLANK_COUNT

    def is_value_range_invalid(self, grid: Any) -> bool:
        """Return True when any cell is outside 0 or 1..16 (AC-FR01-03)."""
        if self.is_size_invalid(grid):
            return False
        if self.is_blank_count_invalid(grid):
            return False
        return self._has_out_of_range_value(grid)

    def is_duplicate_non_zero_invalid(self, grid: Any) -> bool:
        """Return True when non-zero values contain duplicates (AC-FR01-04)."""
        if self.is_size_invalid(grid):
            return False
        if self.is_blank_count_invalid(grid):
            return False
        if self.is_value_range_invalid(grid):
            return False
        return self._has_duplicate_non_zero(grid)

    def _is_invalid_size(self, grid: Any) -> bool:
        if grid is None:
            return True
        if not isinstance(grid, list):
            return True
        if len(grid) != GRID_DIMENSION:
            return True
        for row in grid:
            if not isinstance(row, list):
                return True
            if len(row) != GRID_DIMENSION:
                return True
        return False

    def _count_blanks(self, grid: list[list[int]]) -> int:
        return sum(1 for row in grid for cell in row if cell == CELL_MIN_VALUE)

    def _has_out_of_range_value(self, grid: list[list[int]]) -> bool:
        for row in grid:
            for cell in row:
                if cell == CELL_MIN_VALUE:
                    continue
                if cell < 1 or cell > CELL_MAX_VALUE:
                    return True
        return False

    def _has_duplicate_non_zero(self, grid: list[list[int]]) -> bool:
        seen: set[int] = set()
        for row in grid:
            for cell in row:
                if cell == CELL_MIN_VALUE:
                    continue
                if cell in seen:
                    return True
                seen.add(cell)
        return False
