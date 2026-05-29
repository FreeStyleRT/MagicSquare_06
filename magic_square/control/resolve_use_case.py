"""Orchestrates Boundary validation before Domain resolution."""

from __future__ import annotations

from typing import Any

from magic_square.boundary.contracts import FailureResponse
from magic_square.boundary.validator import BoundaryValidator
from magic_square.control.domain_resolver import DomainResolver


class ResolveUseCase:
    """Boundary-first orchestration (AC-FR01-01, AC-FR01-05)."""

    def __init__(
        self,
        domain_resolver: DomainResolver,
        validator: BoundaryValidator | None = None,
    ) -> None:
        self._domain_resolver = domain_resolver
        self._validator = validator or BoundaryValidator()

    def execute(self, grid: Any) -> FailureResponse | list[int]:
        """Run input validation; call Domain only when size contract passes.

        Args:
            grid: Raw input matrix.

        Returns:
            FailureResponse on size validation failure.
        """
        if self._validator.is_size_invalid(grid):
            return self._validator.validate(grid)
        return self._domain_resolver.resolve(grid)
