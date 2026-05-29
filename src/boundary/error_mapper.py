"""Maps domain outcomes to Boundary failure envelopes (E006)."""

from __future__ import annotations

from src.boundary.contracts import FailureResponse, no_valid_solution_failure


class ErrorMapper:
    """Boundary failure mapper for Control/Domain error translation."""

    @staticmethod
    def map_unsolvable_domain() -> FailureResponse:
        """Return the E006 NO_VALID_SOLUTION failure envelope.

        Returns:
            FailureResponse with NO_VALID_SOLUTION code and message.
        """
        return no_valid_solution_failure()
