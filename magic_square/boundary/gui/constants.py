"""GUI-specific constants derived from Boundary contracts."""

from magic_square.boundary.constants import GRID_DIMENSION

CELL_MIN_VALUE: int = 0
CELL_MAX_VALUE: int = 16
BLANK_VALUE: int = 0
SOLUTION_LENGTH: int = 6

__all__ = [
    "BLANK_VALUE",
    "CELL_MAX_VALUE",
    "CELL_MIN_VALUE",
    "GRID_DIMENSION",
    "SOLUTION_LENGTH",
]
