"""Track B RED skeleton — D-LOC-01, D-MIS-01 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

from entity.services.empty_cell_locator import find_blank_coords  # noqa: F401
from entity.services.missing_number_finder import find_not_exist_nums  # noqa: F401


class TestDLoc01FindBlankCoordsG1:
    """D-LOC-01 — G1 row-major blanks (2,2), (3,3) 1-index."""

    def test_d_loc_01_find_blank_coords_g1_row_major(self) -> None:
        # Given: G1 partial matrix (see tests/entity/conftest.py comments)
        # When: find_blank_coords(matrix)
        pytest.fail("RED: D-LOC-01 — G1 blanks row-major (2,2) then (3,3) 1-index")


class TestDMis01FindNotExistNumsG1:
    """D-MIS-01 — G1 missing numbers {7,10} ascending."""

    def test_d_mis_01_find_not_exist_nums_g1_sorted(self) -> None:
        # Given: G1 partial matrix
        # When: find_not_exist_nums(matrix)
        pytest.fail("RED: D-MIS-01 — G1 missing numbers [7, 10] ascending")
