"""Entity-layer named constants for magic-square domain rules."""

GRID_DIMENSION: int = 4
MATRIX_SIZE: int = GRID_DIMENSION
BLANK_CELL_VALUE: int = 0
REQUIRED_BLANK_COUNT: int = 2
CELL_MIN_VALUE: int = 1
CELL_MAX_VALUE: int = 16


def magic_constant(size: int = MATRIX_SIZE) -> int:
    """Return the magic sum for a square of the given dimension.

    Args:
        size: Grid edge length (default 4 for this project).

    Returns:
        Target sum for each row, column, and diagonal.
    """
    return size * (size * size + 1) // 2


MAGIC_SUM: int = magic_constant(MATRIX_SIZE)
