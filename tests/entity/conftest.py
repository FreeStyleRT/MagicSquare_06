"""G0~G3 grid fixtures for entity/domain tests (Report/09)."""

from __future__ import annotations

import pytest

# G0 — complete 4x4 magic square (M=34)
GRID_G0: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

# G1 — blanks (2,2), (3,3) 1-index; missing {7, 10}
GRID_G1: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 0, 8, 12],
    [9, 6, 0, 4],
    [14, 15, 1, 11],
]

# G2 — PRD D-02; blanks (3,3), (4,4) 1-index
GRID_G2: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# Step-A success grid — attempt 1 (small-first) yields valid magic square
GRID_STEP_A_SUCCESS: list[list[int]] = [
    [16, 2, 3, 13],
    [0, 11, 10, 8],
    [9, 7, 6, 0],
    [4, 14, 15, 1],
]

# G3 — both attempts fail (golden master no_valid_solution)
GRID_G3: list[list[int]] = [
    [0, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 0, 16],
]


@pytest.fixture
def grid_g0() -> list[list[int]]:
    return [row[:] for row in GRID_G0]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    return [row[:] for row in GRID_G1]


@pytest.fixture
def grid_g2() -> list[list[int]]:
    return [row[:] for row in GRID_G2]


@pytest.fixture
def grid_step_a_success() -> list[list[int]]:
    return [row[:] for row in GRID_STEP_A_SUCCESS]


@pytest.fixture
def grid_g3() -> list[list[int]]:
    return [row[:] for row in GRID_G3]
