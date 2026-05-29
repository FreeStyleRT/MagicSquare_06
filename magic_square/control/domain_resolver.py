"""Domain resolution port (solver entry point)."""

from __future__ import annotations


class DomainResolver:
    """Resolves a validated 4x4 grid (FR-05); not invoked on Boundary failure."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Compute magic-square solution for a validated grid.

        Args:
            grid: Validated 4x4 integer matrix.

        Returns:
            Solution as int[6] when implemented.

        Raises:
            NotImplementedError: Solver not implemented in AC-FR01-01 scope.
        """
        raise NotImplementedError("Domain resolve not implemented")
