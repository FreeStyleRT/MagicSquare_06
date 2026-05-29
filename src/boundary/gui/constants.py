"""GUI-specific constants — re-export from Boundary/Entity SSOT."""

from src.boundary.constants import CELL_MAX_VALUE, CELL_MIN_VALUE, GRID_DIMENSION
from src.entity.constants import BLANK_CELL_VALUE
from src.boundary.result_formatter import SOLUTION_LENGTH

BLANK_VALUE: int = BLANK_CELL_VALUE

__all__ = [
    "BLANK_VALUE",
    "CELL_MAX_VALUE",
    "CELL_MIN_VALUE",
    "GRID_DIMENSION",
    "SOLUTION_LENGTH",
]
