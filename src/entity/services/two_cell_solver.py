"""Two-combination solver for partial 4x4 magic squares (FR-05)."""

from __future__ import annotations

import copy

from src.entity.exceptions import UnsolvableDomainError
from src.entity.services.magic_square_validator import is_magic_square
from src.entity.services.partial_grid_analysis import analyze_partial_grid
from src.entity.value_objects.coordinate import Coordinate


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

        attempt_one = self.try_placement(grid, first, second, small, large)
        if attempt_one is not None:
            return attempt_one

        attempt_two = self.try_placement(grid, first, second, large, small)
        if attempt_two is not None:
            return attempt_two

        raise UnsolvableDomainError()

    def try_placement(
        self,
        grid: list[list[int]],
        blank1: Coordinate,
        blank2: Coordinate,
        value1: int,
        value2: int,
    ) -> list[int] | None:
        """Try one blank assignment order; return solution when magic.

        Args:
            grid: Partial 4x4 matrix.
            blank1: First blank coordinate (1-index).
            blank2: Second blank coordinate (1-index).
            value1: Value for the first blank.
            value2: Value for the second blank.

        Returns:
            Six-element solution when the filled grid is magic, else None.
        """
        candidate = self._filled_grid(grid, blank1, value1, blank2, value2)
        if is_magic_square(candidate):
            return _solution_vector(blank1, value1, blank2, value2)
        return None

    def _filled_grid(
        self,
        grid: list[list[int]],
        blank1: Coordinate,
        value1: int,
        blank2: Coordinate,
        value2: int,
    ) -> list[list[int]]:
        candidate = copy.deepcopy(grid)
        candidate[blank1.row - 1][blank1.col - 1] = value1
        candidate[blank2.row - 1][blank2.col - 1] = value2
        return candidate


def _solution_vector(
    blank1: Coordinate,
    value1: int,
    blank2: Coordinate,
    value2: int,
) -> list[int]:
    """Build the six-element FR-05 success vector from blank assignments."""
    return [
        blank1.row,
        blank1.col,
        value1,
        blank2.row,
        blank2.col,
        value2,
    ]


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
