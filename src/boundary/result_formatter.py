"""E007 success vector formatting — Boundary SSOT (R-U3)."""

from __future__ import annotations

from src.boundary.constants import GRID_DIMENSION

SOLUTION_LENGTH: int = 6


class ResultFormatter:
    """Formats solver output as ``int[6]`` with 1-index coordinates."""

    @staticmethod
    def format(
        row1: int,
        col1: int,
        value1: int,
        row2: int,
        col2: int,
        value2: int,
    ) -> list[int]:
        """Build ``[r1, c1, n1, r2, c2, n2]`` from blank assignments.

        Args:
            row1: First blank row (1-index).
            col1: First blank column (1-index).
            value1: Number placed at the first blank.
            row2: Second blank row (1-index).
            col2: Second blank column (1-index).
            value2: Number placed at the second blank.

        Returns:
            Six-element solution vector with 1-index coordinates.
        """
        return [row1, col1, value1, row2, col2, value2]

    @staticmethod
    def is_valid_solution_format(result: list[int]) -> bool:
        """Return True when result satisfies AC-FR05-04 and AC-FR05-05.

        Args:
            result: Candidate six-element solution vector.

        Returns:
            True when length is six and coordinates are 1-index in range.
        """
        if len(result) != SOLUTION_LENGTH:
            return False
        row1, col1, _n1, row2, col2, _n2 = result
        return (
            _is_one_index_in_bounds(row1, col1, GRID_DIMENSION)
            and _is_one_index_in_bounds(row2, col2, GRID_DIMENSION)
        )


def _is_one_index_in_bounds(row: int, col: int, size: int) -> bool:
    """Return True when ``row`` and ``col`` are 1-index coordinates in range."""
    return 1 <= row <= size and 1 <= col <= size
