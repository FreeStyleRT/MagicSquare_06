"""Success result formatting for two-cell solver output (FR-05)."""

from __future__ import annotations

from src.entity.constants import GRID_DIMENSION

Coordinate = tuple[int, int]
SOLUTION_LENGTH: int = 6


class ResultFormatter:
    """Formats solver output as ``int[6]`` with 1-index coordinates."""

    @staticmethod
    def format(
        blank1: Coordinate,
        value1: int,
        blank2: Coordinate,
        value2: int,
    ) -> list[int]:
        """Build ``[r1, c1, n1, r2, c2, n2]`` from blank assignments.

        Args:
            blank1: First blank coordinate (1-index row, col).
            value1: Number placed at the first blank.
            blank2: Second blank coordinate (1-index row, col).
            value2: Number placed at the second blank.

        Returns:
            Six-element solution vector with 1-index coordinates.
        """
        row1, col1 = blank1
        row2, col2 = blank2
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
        coords = (row1, col1, row2, col2)
        return all(1 <= coord <= GRID_DIMENSION for coord in coords)
