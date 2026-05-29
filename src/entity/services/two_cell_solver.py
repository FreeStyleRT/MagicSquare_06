"""Two-combination solver for partial 4x4 magic squares (FR-05)."""

from __future__ import annotations

import copy

from src.entity.exceptions import UnsolvableDomainError
from src.entity.services.partial_grid_analysis import (
    Coordinate,
    analyze_partial_grid,
)
from src.entity.services.magic_square_validator import is_magic_square
from src.entity.services.result_formatter import ResultFormatter


class TwoCellSolver:
    """Attempts small-first then reverse placement for two blank cells."""

    def solve(self, grid: list[list[int]]) -> list[int]:
        """Resolve a partial grid using two fixed assignment attempts.

        Args:
            grid: Validated 4x4 matrix with exactly two blank cells.

        Returns:
            Six-element solution vector ``[r1, c1, n1, r2, c2, n2]``.

        Raises:
            UnsolvableDomainError: When neither attempt yields a magic square.
        """
        context = analyze_partial_grid(grid)
        first, second = context.blanks
        small, large = context.missing

        attempt_one = self._filled_grid(grid, first, small, second, large)
        if is_magic_square(attempt_one):
            return ResultFormatter.format(first, small, second, large)

        attempt_two = self._filled_grid(grid, first, large, second, small)
        if is_magic_square(attempt_two):
            return ResultFormatter.format(first, large, second, small)

        raise UnsolvableDomainError()

    def _filled_grid(
        self,
        grid: list[list[int]],
        blank1: Coordinate,
        value1: int,
        blank2: Coordinate,
        value2: int,
    ) -> list[list[int]]:
        candidate = copy.deepcopy(grid)
        row1, col1 = blank1
        row2, col2 = blank2
        candidate[row1 - 1][col1 - 1] = value1
        candidate[row2 - 1][col2 - 1] = value2
        return candidate


def solution(grid: list[list[int]]) -> list[int]:
    """Solve a partial magic square (FR-05 entry point).

    Args:
        grid: Validated 4x4 matrix with exactly two blank cells.

    Returns:
        Six-element solution vector with 1-index coordinates.

    Raises:
        UnsolvableDomainError: When both attempts fail.
    """
    return TwoCellSolver().solve(grid)
