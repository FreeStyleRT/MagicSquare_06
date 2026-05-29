"""Adapts grid state to ResolveUseCase without Qt dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.boundary.contracts import FailureResponse
from src.control.resolve_use_case import ResolveUseCase

PresenterStatus = Literal["success", "failure", "error"]


@dataclass(frozen=True)
class PresenterOutcome:
    """Result of a solve request for the GUI layer."""

    status: PresenterStatus
    solution: list[int] | None = None
    failure: FailureResponse | None = None
    error_message: str = ""


class GridPresenter:
    """Boundary presenter — wires grid input to Control use case."""

    def __init__(self, use_case: ResolveUseCase) -> None:
        """Initialize with a ResolveUseCase instance.

        Args:
            use_case: Control-layer orchestrator.
        """
        self._use_case = use_case

    def solve(self, grid: list[list[int]]) -> PresenterOutcome:
        """Execute solve flow and map result for display.

        Args:
            grid: 4x4 integer matrix from the grid widget.

        Returns:
            PresenterOutcome with success, failure, or error status.
        """
        try:
            result = self._use_case.execute(grid)
        except NotImplementedError as exc:
            return PresenterOutcome(status="error", error_message=str(exc))
        except Exception as exc:  # noqa: BLE001 — boundary must not crash GUI
            return PresenterOutcome(
                status="error",
                error_message=f"Unexpected error: {exc}",
            )

        if isinstance(result, FailureResponse):
            return PresenterOutcome(status="failure", failure=result)
        return PresenterOutcome(status="success", solution=result)

    @staticmethod
    def format_solution(solution: list[int]) -> str:
        """Format a 6-element solution vector for display.

        Args:
            solution: `[r1, c1, n1, r2, c2, n2]` with 1-index coordinates.

        Returns:
            Human-readable multi-line string.
        """
        r1, c1, n1, r2, c2, n2 = solution
        return (
            f"빈칸 1: 행 {r1}, 열 {c1} → {n1}\n"
            f"빈칸 2: 행 {r2}, 열 {c2} → {n2}\n"
            f"결과: [{r1}, {c1}, {n1}, {r2}, {c2}, {n2}]"
        )
