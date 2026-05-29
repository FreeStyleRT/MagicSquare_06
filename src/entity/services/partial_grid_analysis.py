"""Combined FR-02/FR-03 analysis for two-blank partial grids."""

from __future__ import annotations

from dataclasses import dataclass

from src.entity.constants import (
    BLANK_CELL_VALUE,
    CELL_MAX_VALUE,
    CELL_MIN_VALUE,
    MATRIX_SIZE,
)
from src.entity.value_objects.coordinate import Coordinate


@dataclass(frozen=True)
class PartialGridContext:
    """Row-major blank coordinates and ascending missing numbers."""

    blanks: tuple[Coordinate, Coordinate]
    missing: tuple[int, int]


def analyze_partial_grid(grid: list[list[int]]) -> PartialGridContext:
    """Locate blanks and missing numbers in a single row-major scan.

    Args:
        grid: Validated 4x4 matrix with exactly two blank cells.

    Returns:
        ``PartialGridContext`` with two 1-index blank coords and missing pair.
    """
    coords: list[Coordinate] = []
    present: set[int] = set()
    for row_index in range(MATRIX_SIZE):
        for col_index in range(MATRIX_SIZE):
            cell = grid[row_index][col_index]
            if cell == BLANK_CELL_VALUE:
                coords.append(Coordinate(row_index + 1, col_index + 1))
            else:
                present.add(cell)
    missing = [
        number
        for number in range(CELL_MIN_VALUE, CELL_MAX_VALUE + 1)
        if number not in present
    ]
    return PartialGridContext(
        blanks=(coords[0], coords[1]),
        missing=(missing[0], missing[1]),
    )
