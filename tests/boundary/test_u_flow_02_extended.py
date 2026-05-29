"""Track A RED skeleton — U-FLOW-02 extended (Report/09). Domain execute isolation."""

from __future__ import annotations

import pytest

# Production imports (RED: module may not exist yet)
from boundary.ui_boundary import UIBoundary  # noqa: F401
from control.solve_partial_magic_square import SolvePartialMagicSquare  # noqa: F401


class TestUFlow02InvalidInputNeverCallsExecute:
    """U-FLOW-02 — invalid input → SolvePartialMagicSquare.execute call_count == 0."""

    def test_u_flow_02_null_matrix_execute_not_called(self) -> None:
        # Given: matrix = None
        # spy = <mock/spy on SolvePartialMagicSquare.execute>
        # boundary = UIBoundary(solver=spy_target)
        # When: UIBoundary.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — null matrix must not call execute (call_count == 0)")

    def test_u_flow_02_invalid_size_execute_not_called(self) -> None:
        # Given: matrix = [] or 3x4 grid
        # spy on SolvePartialMagicSquare.execute
        # When: UIBoundary.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — invalid size must not call execute (call_count == 0)")

    def test_u_flow_02_invalid_blank_count_execute_not_called(self) -> None:
        # Given: matrix with blank count != 2 (E002 path)
        # spy on SolvePartialMagicSquare.execute
        # When: UIBoundary.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — invalid blank count must not call execute")

    def test_u_flow_02_invalid_range_execute_not_called(self) -> None:
        # Given: matrix with out-of-range value (E004 path)
        # spy on SolvePartialMagicSquare.execute
        # When: UIBoundary.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — invalid range must not call execute")

    def test_u_flow_02_duplicate_nonzero_execute_not_called(self) -> None:
        # Given: matrix with duplicate non-zero (E005 path)
        # spy on SolvePartialMagicSquare.execute
        # When: UIBoundary.solve(matrix)
        pytest.fail("RED: U-FLOW-02 — duplicate non-zero must not call execute")
