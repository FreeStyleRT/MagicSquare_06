"""Blank coordinate discovery in row-major order (FR-02)."""

from __future__ import annotations

from magic_square.entity.constants import BLANK_CELL_VALUE, GRID_DIMENSION

Coordinate = tuple[int, int]


class BlankFinder:
    """Locates blank (`0`) cell coordinates in row-major scan order."""

    def find(self, grid: list[list[int]]) -> list[Coordinate]:
        """Return blank coordinates as 1-index (row, col) pairs.

        Args:
            grid: Validated 4x4 matrix with exactly two blank cells.

        Returns:
            Two coordinates in row-major scan order.
        """
        coords: list[Coordinate] = []
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                if grid[row][col] == BLANK_CELL_VALUE:
                    coords.append((row + 1, col + 1))
        return coords


def find_blank_coords(grid: list[list[int]]) -> list[Coordinate]:
    """Locate blank cells in row-major order (FR-02 entry point).

    Args:
        grid: Validated 4x4 matrix with exactly two blank cells.

    Returns:
        List of two 1-index (row, col) coordinate tuples.
    """
    return BlankFinder().find(grid)
