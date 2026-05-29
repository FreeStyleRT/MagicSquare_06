"""Sample partial grids for GUI (FR-02/FR-03 SSOT, aligned with Entity test fixtures)."""

from __future__ import annotations

# G1 — blanks (2,2), (3,3) 1-index; missing {7, 10}
GRID_G1: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 0, 8, 12],
    [9, 6, 0, 4],
    [14, 15, 1, 11],
]

# G2 / PRD D-02 — blanks (3,3), (4,4) 1-index
GRID_G2: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

EXAMPLE_GRID: list[list[int]] = GRID_G2
