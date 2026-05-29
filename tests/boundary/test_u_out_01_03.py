"""Track A RED skeleton — U-OUT-01~03 (Report/09). Boundary output contract."""

from __future__ import annotations

import pytest

# Production imports (RED: module may not exist yet)
from boundary.ui_boundary import UIBoundary  # noqa: F401


class TestUOut01SuccessPayloadLengthSix:
    """U-OUT-01 — success result length == 6."""

    def test_u_out_01_success_payload_length_is_six(self) -> None:
        # Given: valid G1 matrix
        # boundary = UIBoundary(domain=<test double returning [2,2,7,3,3,10]>)
        # When: UIBoundary.solve(matrix)
        pytest.fail("RED: U-OUT-01 — success payload length must be 6 (int[6])")


class TestUOut02SuccessCoordinatesOneIndexed:
    """U-OUT-02 — r,c in [1,4] (1-index)."""

    def test_u_out_02_success_coordinates_are_one_indexed(self) -> None:
        # Given: valid G1; mock domain success [2,2,7,3,3,10]
        # When: UIBoundary.solve(matrix)
        pytest.fail("RED: U-OUT-02 — success coordinates r,c must be 1-index in [1,4]")


class TestUOut03SuccessPayloadStructure:
    """U-OUT-03 — success envelope / six int slots contract."""

    def test_u_out_03_success_payload_has_six_integer_slots(self) -> None:
        # Given: valid G1; Control mock returns fixed int[6]
        # When: UIBoundary.solve(matrix)
        pytest.fail("RED: U-OUT-03 — success response exposes six integer values [r1,c1,n1,r2,c2,n2]")
