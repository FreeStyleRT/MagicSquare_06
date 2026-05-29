"""Missing number discovery from validated grids (FR-03)."""

from __future__ import annotations

from src.entity.services.partial_grid_analysis import analyze_partial_grid


class MissingNumberFinder:
    """Finds the two missing numbers from 1..16 in a partial grid."""

    def find(self, grid: list[list[int]]) -> list[int]:
        """Return missing numbers in ascending order.

        Args:
            grid: Validated 4x4 matrix with exactly two blank cells.

        Returns:
            Two missing integers `[small, large]` from the 1..16 range.
        """
        return list(analyze_partial_grid(grid).missing)


def find_not_exist_nums(grid: list[list[int]]) -> list[int]:
    """Locate missing numbers in ascending order (FR-03 entry point).

    Args:
        grid: Validated 4x4 matrix with exactly two blank cells.

    Returns:
        List of two missing integers sorted ascending.
    """
    return MissingNumberFinder().find(grid)
