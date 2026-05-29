"""Input matrix validation at the Boundary layer (FR-01)."""

from __future__ import annotations

from typing import Any

from magic_square.boundary.constants import GRID_DIMENSION
from magic_square.boundary.contracts import FailureResponse, invalid_size_failure


class BoundaryValidator:
    """Validates 4x4 input contract before Domain entry (AC-FR01-01 scope)."""

    def validate(self, grid: Any) -> FailureResponse:
        """Validate grid dimensions; return INVALID_SIZE when not 4x4.

        Args:
            grid: Candidate input matrix.

        Returns:
            FailureResponse when size contract is violated.

        Raises:
            NotImplementedError: When size is valid 4x4 (AC-FR01-02+ not in scope).
        """
        if self.is_size_invalid(grid):
            return invalid_size_failure()
        raise NotImplementedError("AC-FR01-02+ validation not implemented")

    def is_size_invalid(self, grid: Any) -> bool:
        """Return True when grid is not a 4x4 matrix (AC-FR01-01)."""
        return self._is_invalid_size(grid)

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
