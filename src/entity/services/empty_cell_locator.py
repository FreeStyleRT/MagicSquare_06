"""Blank coordinate discovery in row-major order (FR-02)."""

from __future__ import annotations

from src.entity.services.partial_grid_analysis import (
    Coordinate,
    analyze_partial_grid,
)

__all__ = ["BlankFinder", "Coordinate", "find_blank_coords"]


class BlankFinder:
    """Locates blank (`0`) cell coordinates in row-major scan order."""

    def find(self, grid: list[list[int]]) -> list[Coordinate]:
        """Return blank coordinates as 1-index (row, col) pairs.

        Args:
            grid: Validated 4x4 matrix with exactly two blank cells.

        Returns:
            Two coordinates in row-major scan order.
        """
        return list(analyze_partial_grid(grid).blanks)


def find_blank_coords(grid: list[list[int]]) -> list[Coordinate]:
    """Locate blank cells in row-major order (FR-02 entry point).

    Args:
        grid: Validated 4x4 matrix with exactly two blank cells.

    Returns:
        List of two 1-index (row, col) coordinate tuples.
    """
    return BlankFinder().find(grid)
