"""Screen-layer presenter — formats Control outcomes for GUI display."""

from __future__ import annotations

from dataclasses import dataclass

from src.boundary.contracts import FailureResponse
from src.boundary.gui.presenter import PresenterOutcome
from src.boundary.result_formatter import ResultFormatter


@dataclass(frozen=True)
class ResultDisplay:
    """View model for the result panel and status bar."""

    text: str
    stylesheet: str
    status_message: str


class ResultPresenter:
    """Maps ``PresenterOutcome`` to Screen display strings and styles."""

    _STYLE_SUCCESS: str = (
        "color: #1b5e20; background: #e8f5e9; padding: 8px; border-radius: 4px;"
    )
    _STYLE_FAILURE: str = (
        "color: #b71c1c; background: #ffebee; padding: 8px; border-radius: 4px;"
    )
    _STYLE_ERROR: str = (
        "color: #e65100; background: #fff3e0; padding: 8px; border-radius: 4px;"
    )

    @staticmethod
    def format_solution(solution: list[int]) -> str:
        """Format a six-element solution vector for display.

        Args:
            solution: ``[r1, c1, n1, r2, c2, n2]`` with 1-index coordinates.

        Returns:
            Human-readable multi-line string.
        """
        r1, c1, n1, r2, c2, n2 = solution
        return (
            f"빈칸 1: 행 {r1}, 열 {c1} → {n1}\n"
            f"빈칸 2: 행 {r2}, 열 {c2} → {n2}\n"
            f"결과: [{r1}, {c1}, {n1}, {r2}, {c2}, {n2}]"
        )

    @classmethod
    def format_outcome(cls, outcome: PresenterOutcome) -> ResultDisplay:
        """Build result panel content from a solve outcome.

        Args:
            outcome: Boundary presenter result.

        Returns:
            ``ResultDisplay`` for the result label and status bar.
        """
        if outcome.status == "success" and outcome.solution is not None:
            return ResultDisplay(
                text=cls.format_solution(outcome.solution),
                stylesheet=cls._STYLE_SUCCESS,
                status_message="풀이 성공",
            )

        if outcome.status == "failure" and outcome.failure is not None:
            return cls._format_failure(outcome.failure)

        message = outcome.error_message or "알 수 없는 오류가 발생했습니다."
        return ResultDisplay(
            text=f"처리 불가: {message}",
            stylesheet=cls._STYLE_ERROR,
            status_message="내부 오류",
        )

    @classmethod
    def _format_failure(cls, failure: FailureResponse) -> ResultDisplay:
        return ResultDisplay(
            text=(
                f"오류 코드: {failure.code}\n"
                f"메시지: {failure.message}"
            ),
            stylesheet=cls._STYLE_FAILURE,
            status_message=f"검증 실패 — {failure.code}",
        )

    @staticmethod
    def is_valid_solution(solution: list[int]) -> bool:
        """Return True when solution satisfies E007 int[6] contract."""
        return ResultFormatter.is_valid_solution_format(solution)
