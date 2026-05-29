"""Golden Master scenario definitions (PRD §16.4, Report/09 G1~G3)."""

from __future__ import annotations

from dataclasses import dataclass

from tests.conftest import GRID_DUPLICATE_NON_ZERO, GRID_THREE_BLANKS

GRID_NORMAL_SUCCESS: list[list[int]] = [
    [0, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

GRID_REVERSE_SUCCESS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# G3 placeholder — exactly two blanks; domain unsolvable when implemented.
GRID_NO_VALID_SOLUTION: list[list[int]] = [
    [0, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 0, 16],
]


@dataclass(frozen=True)
class GoldenScenario:
    """One Golden Master input/output contract."""

    section_id: str
    grid: list[list[int]]


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario(section_id="normal_success", grid=GRID_NORMAL_SUCCESS),
    GoldenScenario(section_id="reverse_success", grid=GRID_REVERSE_SUCCESS),
    GoldenScenario(
        section_id="invalid_blank_count",
        grid=GRID_THREE_BLANKS,
    ),
    GoldenScenario(
        section_id="duplicate_number",
        grid=GRID_DUPLICATE_NON_ZERO,
    ),
    GoldenScenario(
        section_id="no_valid_solution",
        grid=GRID_NO_VALID_SOLUTION,
    ),
)
