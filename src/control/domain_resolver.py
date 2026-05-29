"""Domain resolution port (solver entry point)."""

from __future__ import annotations

from src.control.solution_result import SolutionResult
from src.entity.services.partial_grid_analysis import (
    PartialGridContext,
    analyze_partial_grid,
)
from src.entity.services.two_cell_solver import TwoCellSolver


class DomainResolver:
    """Resolves a validated 4x4 grid via Entity-layer TwoCellSolver (FR-05)."""

    def __init__(self, solver: TwoCellSolver | None = None) -> None:
        """Initialize with injectable solver for testing.

        Args:
            solver: Entity-layer two-cell solver; defaults to production wiring.
        """
        self._solver = solver or TwoCellSolver()

    def resolve(self, grid: list[list[int]]) -> SolutionResult:
        """Compute magic-square solution for a validated grid.

        Args:
            grid: Validated 4x4 integer matrix.

        Returns:
            ``SolutionResult`` with six-element vector ``[r1, c1, n1, r2, c2, n2]``.

        Raises:
            UnsolvableDomainError: When both solver attempts fail.
        """
        return SolutionResult.wrap(self._solver.solve(grid))

    def analyze(self, grid: list[list[int]]) -> PartialGridContext:
        """Locate blanks and missing numbers for a validated partial grid.

        Args:
            grid: Validated 4x4 integer matrix.

        Returns:
            Combined FR-02/FR-03 snapshot from a single row-major scan.
        """
        return analyze_partial_grid(grid)
