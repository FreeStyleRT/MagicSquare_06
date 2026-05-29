"""Golden Master approve-pattern utilities for solver regression tests."""

from __future__ import annotations

import difflib
from pathlib import Path
from typing import Any

from magic_square.boundary.contracts import FailureResponse
from magic_square.control.resolve_use_case import ResolveUseCase

from tests.helpers.golden_scenarios import GOLDEN_SCENARIOS, GoldenScenario

GOLDEN_MASTER_PATH: Path = Path(__file__).resolve().parent.parent / (
    "golden_master_expected.txt"
)

NOT_IMPLEMENTED_CODE: str = "NOT_IMPLEMENTED"


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
    try:
        result = use_case.execute(grid)
    except NotImplementedError:
        return f"Error:\n{NOT_IMPLEMENTED_CODE}"

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
        if line.startswith("[") and line.endswith("]"):
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
        golden_path.write_text(actual_document, encoding="utf-8")
        return

    expected_document = golden_path.read_text(encoding="utf-8")
    if actual_document == expected_document:
        return

    diff_text = unified_diff(
        expected_document,
        actual_document,
        fromfile=str(golden_path),
        tofile="current output",
    )
    raise AssertionError(
        "Golden Master mismatch. Re-run with --golden-approve to update.\n"
        f"{diff_text}",
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
