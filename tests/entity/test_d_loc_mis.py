"""Track B — D-LOC-01 (FR-02), D-MIS-01 (FR-03)."""

from __future__ import annotations

from magic_square.entity.services.empty_cell_locator import (
    BlankFinder,
    find_blank_coords,
)
from magic_square.entity.services.missing_number_finder import (
    MissingNumberFinder,
    find_not_exist_nums,
)
from tests.entity.conftest import GRID_G1, GRID_G2


class TestDLoc01FindBlankCoordsG1:
    """D-LOC-01 — G1 row-major blanks (2,2), (3,3) 1-index."""

    def test_d_loc_01_find_blank_coords_g1_row_major(
        self,
        grid_g1: list[list[int]],
    ) -> None:
        # Given: G1 partial matrix
        # When: find_blank_coords(matrix)
        result = find_blank_coords(grid_g1)

        # Then: row-major 1-index blanks
        assert result == [(2, 2), (3, 3)]


class TestBlankFinderG2:
    """AC-FR02-01~03 — G2 (PRD D-02) blank discovery."""

    def test_find_blank_coords_g2_row_major(self, grid_g2: list[list[int]]) -> None:
        result = find_blank_coords(grid_g2)

        assert result == [(3, 3), (4, 4)]

    def test_blank_finder_class_matches_function(self, grid_g2: list[list[int]]) -> None:
        finder = BlankFinder()

        assert finder.find(grid_g2) == find_blank_coords(grid_g2)


class TestBlankFinderContract:
    """AC-FR02-01~03 — count, order, and first-blank invariants."""

    def test_returns_exactly_two_coordinates(self, grid_g1: list[list[int]]) -> None:
        result = find_blank_coords(grid_g1)

        assert len(result) == 2

    def test_first_blank_matches_row_major_scan(self, grid_g1: list[list[int]]) -> None:
        first_zero: tuple[int, int] | None = None
        for row in range(len(grid_g1)):
            for col in range(len(grid_g1[row])):
                if grid_g1[row][col] == 0:
                    first_zero = (row + 1, col + 1)
                    break
            if first_zero is not None:
                break

        result = find_blank_coords(grid_g1)

        assert result[0] == first_zero

    def test_row_major_order_preserved(self, grid_g2: list[list[int]]) -> None:
        result = find_blank_coords(grid_g2)

        assert result[0][0] < result[1][0] or (
            result[0][0] == result[1][0] and result[0][1] < result[1][1]
        )


class TestDMis01FindNotExistNumsG1:
    """D-MIS-01 — G1 missing numbers {7,10} ascending."""

    def test_d_mis_01_find_not_exist_nums_g1_sorted(
        self,
        grid_g1: list[list[int]],
    ) -> None:
        # Given: G1 partial matrix
        # When: find_not_exist_nums(matrix)
        result = find_not_exist_nums(grid_g1)

        # Then: ascending missing numbers
        assert result == [7, 10]


class TestMissingNumberFinderG2:
    """AC-FR03 — G2 (PRD D-02) missing number discovery."""

    def test_find_not_exist_nums_g2_sorted(self, grid_g2: list[list[int]]) -> None:
        result = find_not_exist_nums(grid_g2)

        assert result == [1, 6]

    def test_missing_number_finder_class_matches_function(
        self,
        grid_g2: list[list[int]],
    ) -> None:
        finder = MissingNumberFinder()

        assert finder.find(grid_g2) == find_not_exist_nums(grid_g2)


class TestMissingNumberFinderContract:
    """AC-FR03-01~03 — count, sort order, and range invariants."""

    def test_returns_exactly_two_missing_numbers(
        self,
        grid_g1: list[list[int]],
    ) -> None:
        result = find_not_exist_nums(grid_g1)

        assert len(result) == 2

    def test_missing_numbers_are_ascending(self, grid_g1: list[list[int]]) -> None:
        result = find_not_exist_nums(grid_g1)

        assert result[0] < result[1]

    def test_missing_numbers_are_within_one_to_sixteen(
        self,
        grid_g1: list[list[int]],
    ) -> None:
        result = find_not_exist_nums(grid_g1)

        assert all(1 <= number <= 16 for number in result)

    def test_zeros_are_excluded_from_present_set(self, grid_g1: list[list[int]]) -> None:
        result = find_not_exist_nums(grid_g1)

        assert 0 not in result
