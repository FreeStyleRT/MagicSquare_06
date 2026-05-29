"""Control-layer SSOT for FR-05 success vectors (int[6])."""

from __future__ import annotations

from dataclasses import dataclass

from src.entity.services.result_formatter import SOLUTION_LENGTH


@dataclass(frozen=True)
class SolutionResult:
    """Canonical six-element success payload from Domain resolution."""

    values: tuple[int, int, int, int, int, int]

    @classmethod
    def wrap(cls, raw: list[int]) -> SolutionResult:
        """Wrap Entity solver output as the Control SSOT.

        Args:
            raw: Solver output ``[r1, c1, n1, r2, c2, n2]``.

        Returns:
            Immutable ``SolutionResult`` with validated length.

        Raises:
            ValueError: When ``raw`` is not a six-element vector.
        """
        if len(raw) != SOLUTION_LENGTH:
            msg = f"Solution vector length must be {SOLUTION_LENGTH}, got {len(raw)}"
            raise ValueError(msg)
        return cls(
            values=(raw[0], raw[1], raw[2], raw[3], raw[4], raw[5]),
        )

    def to_list(self) -> list[int]:
        """Return a list copy for boundary serialization."""
        return list(self.values)
