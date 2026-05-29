"""Entity magic constants and grid sum helpers (R-L2, R-L3)."""

from __future__ import annotations

from src.entity.constants import MAGIC_SUM, MATRIX_SIZE, magic_constant
from src.entity.services.grid_sums import (
    is_magic_sum,
    sum_anti_diagonal,
    sum_col,
    sum_main_diagonal,
    sum_row,
)
from tests.entity.conftest import GRID_G0


class TestMagicConstant:
    """R-L3 — magic constant derived from matrix size."""

    def test_magic_constant_for_4x4_is_34(self) -> None:
        assert magic_constant(MATRIX_SIZE) == 34
        assert MAGIC_SUM == 34


class TestGridSums:
    """R-L2 — row/column/diagonal sum helpers."""

    def test_g0_row_sums_match_magic_constant(self, grid_g0: list[list[int]]) -> None:
        for row_index in range(MATRIX_SIZE):
            assert is_magic_sum(sum_row(grid_g0, row_index))

    def test_g0_col_sums_match_magic_constant(self, grid_g0: list[list[int]]) -> None:
        for col_index in range(MATRIX_SIZE):
            assert is_magic_sum(sum_col(grid_g0, col_index))

    def test_g0_diagonal_sums_match_magic_constant(self, grid_g0: list[list[int]]) -> None:
        assert is_magic_sum(sum_main_diagonal(grid_g0))
        assert is_magic_sum(sum_anti_diagonal(grid_g0))
