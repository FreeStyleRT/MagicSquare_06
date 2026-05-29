"""1-index grid coordinate value object (FR-02, FR-05)."""

from __future__ import annotations

from typing import NamedTuple

from src.entity.constants import MATRIX_SIZE


class Coordinate(NamedTuple):
    """One-index ``(row, col)`` pair on a 4x4 grid."""

    row: int
    col: int

    def is_in_bounds(self, size: int = MATRIX_SIZE) -> bool:
        """Return True when both components are within ``1..size``.

        Args:
            size: Grid edge length.

        Returns:
            True when row and col are valid 1-index coordinates.
        """
        return all(1 <= component <= size for component in (self.row, self.col))
