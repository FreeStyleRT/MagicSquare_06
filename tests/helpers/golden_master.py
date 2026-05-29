"""Golden Master approve-pattern utilities for solver regression tests."""

from __future__ import annotations

import difflib
import re
from pathlib import Path
_SECTION_HEADER_PATTERN = re.compile(r"^\[[a-z_]+\]$")

from src.boundary.contracts import (
    DUPLICATE_NON_ZERO_CODE,
    DUPLICATE_NON_ZERO_MESSAGE,
    FailureResponse,
    INVALID_BLANK_COUNT_CODE,
    INVALID_BLANK_COUNT_MESSAGE,
    NO_VALID_SOLUTION_CODE,
    NO_VALID_SOLUTION_MESSAGE,
    duplicate_non_zero_failure,
    invalid_blank_count_failure,
    no_valid_solution_failure,
)
from src.control.resolve_use_case import ResolveUseCase
from src.entity.services.partial_grid_analysis import analyze_partial_grid
from src.entity.services.magic_square_validator import is_magic_square
from src.boundary.result_formatter import ResultFormatter
from src.entity.services.two_cell_solver import TwoCellSolver

from tests.helpers.golden_scenarios import GOLDEN_SCENARIOS, GoldenScenario

GOLDEN_MASTER_PATH: Path = Path(__file__).resolve().parent.parent / (
    "golden_master_expected.txt"
)

DEFAULT_GOLDEN_MASTER_PATH: Path = GOLDEN_MASTER_PATH

GOLDEN_ERROR_CONTRACTS: dict[str, tuple[str, str]] = {
    "invalid_blank_count": (
        INVALID_BLANK_COUNT_CODE,
        INVALID_BLANK_COUNT_MESSAGE,
    ),
    "duplicate_number": (
        DUPLICATE_NON_ZERO_CODE,
        DUPLICATE_NON_ZERO_MESSAGE,
    ),
    "no_valid_solution": (
        NO_VALID_SOLUTION_CODE,
        NO_VALID_SOLUTION_MESSAGE,
    ),
}

GOLDEN_FAILURE_FACTORIES: dict[str, FailureResponse] = {
    "invalid_blank_count": invalid_blank_count_failure(),
    "duplicate_number": duplicate_non_zero_failure(),
    "no_valid_solution": no_valid_solution_failure(),
}


def format_grid(grid: list[list[int]]) -> str:
    """Serialize a 4x4 grid as space-separated rows.

    Args:
        grid: Input matrix.

    Returns:
        Multi-line text block for golden files.
    """
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def format_solution(solution: list[int]) -> str:
    """Serialize a six-element solution vector in compact form.

    Args:
        solution: ``[r1, c1, n1, r2, c2, n2]`` with 1-index coordinates.

    Returns:
        Bracketed comma-separated values without spaces.
    """
    return "[" + ",".join(str(value) for value in solution) + "]"


def capture_resolve_output(
    use_case: ResolveUseCase,
    grid: list[list[int]],
) -> str:
    """Run ResolveUseCase and serialize the result for golden comparison.

    Args:
        use_case: Control-layer orchestrator wired like production.
        grid: Scenario input matrix.

    Returns:
        ``Output:`` or ``Error:`` block text.
    """
    result = use_case.execute(grid)

    if isinstance(result, FailureResponse):
        return f"Error:\n{result.code}"
    return f"Output:\n{format_solution(result)}"


def format_scenario_block(
    scenario: GoldenScenario,
    body: str,
) -> str:
    """Build one golden-master section.

    Args:
        scenario: Scenario metadata.
        body: Captured ``Output:`` or ``Error:`` block.

    Returns:
        Full section text including header and input grid.
    """
    return (
        f"[{scenario.section_id}]\n"
        f"Input:\n"
        f"{format_grid(scenario.grid)}\n"
        f"{body}"
    )


def build_golden_document(
    use_case: ResolveUseCase,
    scenarios: tuple[GoldenScenario, ...] = GOLDEN_SCENARIOS,
) -> str:
    """Capture all scenarios and assemble the golden-master file body.

    Args:
        use_case: Control-layer orchestrator.
        scenarios: Scenario registry.

    Returns:
        Full golden document text ending with a trailing newline.
    """
    blocks = [
        format_scenario_block(
            scenario,
            capture_resolve_output(use_case, scenario.grid),
        )
        for scenario in scenarios
    ]
    return "\n\n".join(blocks) + "\n"


def _is_section_header(line: str) -> bool:
    """Return True when ``line`` is a scenario section header.

    Args:
        line: Single line from a golden document.

    Returns:
        True for ``[section_id]`` headers; false for compact ``Output`` vectors.
    """
    return bool(_SECTION_HEADER_PATTERN.match(line))


def parse_golden_document(text: str) -> dict[str, str]:
    """Parse a golden-master document into section-id → body maps.

    Args:
        text: Golden file contents.

    Returns:
        Mapping of section id to full section text.
    """
    sections: dict[str, str] = {}
    current_id: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if _is_section_header(line):
            if current_id is not None:
                sections[current_id] = "\n".join(current_lines).rstrip()
            current_id = line[1:-1]
            current_lines = [line]
            continue
        if current_id is not None:
            current_lines.append(line)

    if current_id is not None:
        sections[current_id] = "\n".join(current_lines).rstrip()

    return sections


def unified_diff(
    expected: str,
    actual: str,
    *,
    fromfile: str = "expected",
    tofile: str = "actual",
) -> str:
    """Return unified diff text for a golden mismatch.

    Args:
        expected: Baseline section or document.
        actual: Current captured section or document.
        fromfile: Left-hand diff label.
        tofile: Right-hand diff label.

    Returns:
        Unified diff string; empty when contents match.
    """
    expected_lines = expected.splitlines(keepends=True)
    actual_lines = actual.splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            expected_lines,
            actual_lines,
            fromfile=fromfile,
            tofile=tofile,
            lineterm="",
        ),
    )


def approve_golden_master(
    actual: str,
    golden_path: Path,
    *,
    auto_create: bool = True,
    force_update: bool = False,
) -> str:
    """Write or compare a golden-master baseline document.

    Args:
        actual: Captured golden document text.
        golden_path: Path to the committed baseline file.
        auto_create: When True, create the file if it does not exist.
        force_update: When True, overwrite the file when content differs.

    Returns:
        ``"created"``, ``"updated"``, or ``"matched"``.

    Raises:
        AssertionError: When the baseline is missing (and not auto-created) or
            when content differs and ``force_update`` is False.
    """
    if not golden_path.exists():
        if not auto_create:
            raise AssertionError(
                f"Golden Master baseline not found: {golden_path}. "
                "Run without --check to create it.",
            )
        golden_path.write_text(actual, encoding="utf-8")
        return "created"

    expected = golden_path.read_text(encoding="utf-8")
    if actual == expected:
        return "matched"

    if force_update:
        golden_path.write_text(actual, encoding="utf-8")
        return "updated"

    diff_text = unified_diff(
        expected,
        actual,
        fromfile=str(golden_path),
        tofile="current output",
    )
    raise AssertionError(
        "Golden Master mismatch. Re-run without --check to update.\n"
        f"{diff_text}",
    )


def assert_golden_master(
    use_case: ResolveUseCase,
    *,
    golden_path: Path = GOLDEN_MASTER_PATH,
    approve: bool = False,
    scenarios: tuple[GoldenScenario, ...] = GOLDEN_SCENARIOS,
) -> None:
    """Compare or approve the golden-master baseline.

    Args:
        use_case: Control-layer orchestrator.
        golden_path: Path to the committed baseline file.
        approve: When True, overwrite the baseline with current output.
        scenarios: Scenario registry.

    Raises:
        AssertionError: When actual output does not match the baseline.
    """
    actual_document = build_golden_document(use_case, scenarios)

    if approve or not golden_path.exists():
        approve_golden_master(
            actual_document,
            golden_path,
            auto_create=True,
            force_update=True,
        )
        return

    approve_golden_master(
        actual_document,
        golden_path,
        auto_create=False,
        force_update=False,
    )


def load_section_bodies(document: str) -> dict[str, str]:
    """Extract scenario bodies keyed by section id.

    Args:
        document: Golden document text.

    Returns:
        Section id to body without the ``[id]`` header line.
    """
    parsed = parse_golden_document(document)
    return {
        section_id: "\n".join(body.splitlines()[1:]).strip()
        for section_id, body in parsed.items()
    }


def build_scenario_block(
    use_case: ResolveUseCase,
    scenario: GoldenScenario,
) -> str:
    """Capture one scenario as a golden section block.

    Args:
        use_case: Control-layer orchestrator.
        scenario: Scenario metadata and input grid.

    Returns:
        Full section text including header and input grid.
    """
    body = capture_resolve_output(use_case, scenario.grid)
    return format_scenario_block(scenario, body)


def assert_golden_section(
    use_case: ResolveUseCase,
    scenario: GoldenScenario,
    *,
    golden_path: Path = GOLDEN_MASTER_PATH,
    approve: bool = False,
) -> None:
    """Compare or approve one golden-master scenario section.

    Args:
        use_case: Control-layer orchestrator.
        scenario: Scenario to capture and compare.
        golden_path: Path to the committed baseline file.
        approve: When True, overwrite the baseline with current output.

    Raises:
        AssertionError: When actual output does not match the baseline section.
    """
    if approve or not golden_path.exists():
        assert_golden_master(
            use_case,
            golden_path=golden_path,
            approve=approve or not golden_path.exists(),
        )
        return

    expected_document = golden_path.read_text(encoding="utf-8")
    expected_sections = parse_golden_document(expected_document)
    actual_block = build_scenario_block(use_case, scenario)

    if scenario.section_id not in expected_sections:
        diff_text = unified_diff(
            "",
            actual_block,
            fromfile=f"{scenario.section_id} (missing)",
            tofile=f"{scenario.section_id} (actual)",
        )
        raise AssertionError(
            f"Golden Master section [{scenario.section_id}] missing in "
            f"{golden_path}. Re-run with --golden-approve to update.\n"
            f"{diff_text}",
        )

    expected_block = expected_sections[scenario.section_id]
    if actual_block == expected_block:
        return

    diff_text = compare_section(
        expected_block,
        actual_block,
        section_id=scenario.section_id,
    )
    raise AssertionError(
        f"Golden Master mismatch [{scenario.section_id}]. "
        "Re-run with --golden-approve to update.\n"
        f"{diff_text}",
    )


def assert_success_output_contract(
    result: list[int],
    grid: list[list[int]],
    *,
    require_reverse_fallback: bool = False,
) -> None:
    """Assert FR-05 success vector and placement rules.

    Args:
        result: Six-element solution from ``ResolveUseCase``.
        grid: Scenario input matrix.
        require_reverse_fallback: When True, assert attempt 1 fails and
            attempt 2 (reverse assignment) succeeds.

    Raises:
        AssertionError: When format or placement contracts are violated.
    """
    assert len(result) == 6
    assert ResultFormatter.is_valid_solution_format(result)

    context = analyze_partial_grid(grid)
    first, second = context.blanks
    small, large = context.missing
    assert (result[0], result[1]) == first
    assert (result[3], result[4]) == second

    solver = TwoCellSolver()
    attempt_one = solver._filled_grid(grid, first, small, second, large)
    attempt_two = solver._filled_grid(grid, first, large, second, small)

    if require_reverse_fallback:
        assert is_magic_square(attempt_one) is False
        assert is_magic_square(attempt_two) is True
        assert result == ResultFormatter.format(
            first.row, first.col, large, second.row, second.col, small,
        )
        return

    assert is_magic_square(attempt_one) or is_magic_square(attempt_two)
    if is_magic_square(attempt_one):
        assert result == ResultFormatter.format(
            first.row, first.col, small, second.row, second.col, large,
        )
    else:
        assert result == ResultFormatter.format(
            first.row, first.col, large, second.row, second.col, small,
        )


def assert_error_output_contract(
    result: FailureResponse,
    scenario: GoldenScenario,
) -> None:
    """Assert FR-01 failure envelope for a golden error scenario.

    Args:
        result: Failure response from ``ResolveUseCase``.
        scenario: Golden scenario metadata.

    Raises:
        AssertionError: When code or message does not match the contract.
    """
    expected_code, expected_message = GOLDEN_ERROR_CONTRACTS[scenario.section_id]
    assert result.code == expected_code
    assert result.message == expected_message
    canonical = GOLDEN_FAILURE_FACTORIES[scenario.section_id]
    assert result == canonical


def assert_scenario_output_contract(
    use_case: ResolveUseCase,
    scenario: GoldenScenario,
) -> None:
    """Validate API result contracts for one golden scenario.

    Args:
        use_case: Control-layer orchestrator.
        scenario: Scenario metadata.

    Raises:
        AssertionError: When result type or domain contracts are violated.
    """
    result = use_case.execute(scenario.grid)
    if scenario.section_id in GOLDEN_ERROR_CONTRACTS:
        assert isinstance(result, FailureResponse)
        assert_error_output_contract(result, scenario)
        return

    assert isinstance(result, list)
    require_reverse = scenario.section_id == "reverse_success"
    assert_success_output_contract(
        result,
        scenario.grid,
        require_reverse_fallback=require_reverse,
    )


def compare_section(
    expected_body: str,
    actual_body: str,
    *,
    section_id: str,
) -> str:
    """Return unified diff for one scenario section body.

    Args:
        expected_body: Baseline body text.
        actual_body: Captured body text.
        section_id: Scenario identifier for diff labels.

    Returns:
        Unified diff string; empty when bodies match.
    """
    return unified_diff(
        expected_body,
        actual_body,
        fromfile=f"{section_id} (expected)",
        tofile=f"{section_id} (actual)",
    )
