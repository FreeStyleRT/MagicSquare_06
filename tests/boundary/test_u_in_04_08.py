"""Track A RED skeleton — U-IN-04~08 (Report/09). FR-01 input validation extensions."""

from __future__ import annotations

import pytest

# Production imports (RED: module may not exist yet — collection ERROR is valid RED)
from boundary.input_validator import InputValidator  # noqa: F401


class TestUIn04ZeroEmptyCellsReturnsE002:
    """U-IN-04 — blank count 0 → E002."""

    def test_u_in_04_zero_empty_cells_returns_e002(self) -> None:
        # Given: G1 variant with no zeros (16 filled cells)
        # validator = InputValidator()
        # matrix = <16-cell grid, zero blanks>
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-04 — zero blank cells → E002 failure envelope")


class TestUIn05ThreeBlanksReturnsE002:
    """U-IN-05 — blank count 3 → E002."""

    def test_u_in_05_three_blanks_returns_e002(self) -> None:
        # Given: 4x4 grid with three zeros
        # validator = InputValidator()
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-05 — three blank cells → E002 failure envelope")


class TestUIn06ValueBelowRangeReturnsE004:
    """U-IN-06 — value -1 → E004."""

    def test_u_in_06_value_below_range_returns_e004(self) -> None:
        # Given: G1 with -1 inserted (e.g. matrix[1][2] = -1)
        # validator = InputValidator()
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-06 — value below 1..16 → E004 failure envelope")


class TestUIn07ValueAboveRangeReturnsE004:
    """U-IN-07 — value 17 → E004."""

    def test_u_in_07_value_above_range_returns_e004(self) -> None:
        # Given: G1 with 17 inserted (e.g. matrix[0][0] = 17)
        # validator = InputValidator()
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-07 — value above 1..16 → E004 failure envelope")


class TestUIn08DuplicateNonZeroReturnsE005:
    """U-IN-08 — duplicate non-zero → E005."""

    def test_u_in_08_duplicate_nonzero_returns_e005(self) -> None:
        # Given: G1 with duplicate non-zero (e.g. second 2 in row 0)
        # validator = InputValidator()
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-08 — duplicate non-zero → E005 failure envelope")
