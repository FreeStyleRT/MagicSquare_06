"""Domain resolution port (solver entry point)."""

from __future__ import annotations

from magic_square.entity.services.two_cell_solver import TwoCellSolver


class DomainResolver:
    """Resolves a validated 4x4 grid via Entity-layer TwoCellSolver (FR-05)."""

    def __init__(self, solver: TwoCellSolver | None = None) -> None:
        """Initialize with injectable solver for testing.

        Args:
            solver: Entity-layer two-cell solver; defaults to production wiring.
        """
        self._solver = solver or TwoCellSolver()

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Compute magic-square solution for a validated grid.

        Args:
            grid: Validated 4x4 integer matrix.

        Returns:
            Six-element solution vector ``[r1, c1, n1, r2, c2, n2]``.

        Raises:
            UnsolvableDomainError: When both solver attempts fail.
        """
        return self._solver.solve(grid)
