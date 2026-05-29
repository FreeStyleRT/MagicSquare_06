"""Orchestrates Boundary validation before Domain resolution."""

from __future__ import annotations

from typing import Any

from src.boundary.contracts import FailureResponse
from src.boundary.error_mapper import ErrorMapper
from src.boundary.validator import BoundaryValidator
from src.control.domain_resolver import DomainResolver
from src.entity.exceptions import UnsolvableDomainError


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
        """Run FR-01 validation; call Domain only when all checks pass.

        Args:
            grid: Raw input matrix.

        Returns:
            FailureResponse on FR-01 validation or domain unsolvable failure.
            Six-element solution list when solve succeeds.
        """
        failure = self._validator.validation_failure(grid)
        if failure is not None:
            return failure
        try:
            return self._domain_resolver.resolve(grid).to_list()
        except UnsolvableDomainError:
            return ErrorMapper.map_unsolvable_domain()
