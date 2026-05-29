"""Row, column, and diagonal sum helpers for magic-square validation."""

from __future__ import annotations

from src.entity.constants import GRID_DIMENSION, MAGIC_SUM


def sum_row(grid: list[list[int]], row_index: int) -> int:
    """Return the sum of one row.

    Args:
        grid: Square matrix.
        row_index: Zero-based row index.

    Returns:
        Row sum.
    """
    return sum(grid[row_index])


def sum_col(grid: list[list[int]], col_index: int) -> int:
    """Return the sum of one column.

    Args:
        grid: Square matrix.
        col_index: Zero-based column index.

    Returns:
        Column sum.
    """
    return sum(grid[row][col_index] for row in range(GRID_DIMENSION))


def sum_main_diagonal(grid: list[list[int]]) -> int:
    """Return the main diagonal sum (top-left to bottom-right).

    Args:
        grid: Square matrix.

    Returns:
        Main diagonal sum.
    """
    return sum(grid[index][index] for index in range(GRID_DIMENSION))


def sum_anti_diagonal(grid: list[list[int]]) -> int:
    """Return the anti-diagonal sum (top-right to bottom-left).

    Args:
        grid: Square matrix.

    Returns:
        Anti-diagonal sum.
    """
    return sum(
        grid[index][GRID_DIMENSION - 1 - index] for index in range(GRID_DIMENSION)
    )


def is_magic_sum(total: int) -> bool:
    """Return True when ``total`` equals the domain magic constant.

    Args:
        total: Candidate row, column, or diagonal sum.

    Returns:
        True when ``total`` matches ``MAGIC_SUM``.
    """
    return total == MAGIC_SUM
