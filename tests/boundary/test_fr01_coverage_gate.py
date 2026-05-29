"""TP-REF-01 / G-21 — P0·P1 regression + Boundary/Control coverage gate (no REFACTOR)."""

from __future__ import annotations

import subprocess
import sys


class TestAcFr0101CoverageGate:
    """AC-FR01-01 scoped gate: FR01 tests pass with boundary/control cov >= 85%."""

    def test_p0_p1_regression_with_boundary_control_cov_gate(self) -> None:
        # G-21 / TP-REF-01
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "tests/boundary/test_fr01_invalid_size.py",
            "tests/boundary/test_u_in_04_08.py",
            "tests/boundary/test_u_flow_02_extended.py",
            "tests/control/test_fr01_domain_not_called.py",
            "--cov=magic_square.boundary",
            "--cov=magic_square.control",
            "--cov-fail-under=85",
            "-q",
        ]
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, (
            "P0·P1 cov gate failed\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
