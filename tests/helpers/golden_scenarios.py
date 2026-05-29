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
    test_case_id: str = ""


def scenario_by_section(section_id: str) -> GoldenScenario:
    """Return the scenario registered for a golden section id.

    Args:
        section_id: Section key from ``golden_master_expected.txt``.

    Returns:
        Matching scenario definition.

    Raises:
        KeyError: When ``section_id`` is unknown.
    """
    for scenario in GOLDEN_SCENARIOS:
        if scenario.section_id == section_id:
            return scenario
    raise KeyError(section_id)


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario(
        section_id="normal_success",
        grid=GRID_NORMAL_SUCCESS,
        test_case_id="GM-TC-01",
    ),
    GoldenScenario(
        section_id="reverse_success",
        grid=GRID_REVERSE_SUCCESS,
        test_case_id="GM-TC-02",
    ),
    GoldenScenario(
        section_id="invalid_blank_count",
        grid=GRID_THREE_BLANKS,
        test_case_id="GM-TC-03",
    ),
    GoldenScenario(
        section_id="duplicate_number",
        grid=GRID_DUPLICATE_NON_ZERO,
        test_case_id="GM-TC-04",
    ),
    GoldenScenario(
        section_id="no_valid_solution",
        grid=GRID_NO_VALID_SOLUTION,
        test_case_id="GM-TC-05",
    ),
)

# GM-2 parametrization: (test case id, section id)
GOLDEN_TEST_CASES: tuple[tuple[str, str], ...] = tuple(
    (scenario.test_case_id, scenario.section_id) for scenario in GOLDEN_SCENARIOS
)
