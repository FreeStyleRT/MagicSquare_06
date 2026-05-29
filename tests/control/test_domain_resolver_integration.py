"""Integration tests for DomainResolver wiring (FR-02~FR-05 assembly)."""

from __future__ import annotations

from src.boundary.contracts import NO_VALID_SOLUTION_CODE
from src.control.domain_resolver import DomainResolver
from src.control.resolve_use_case import ResolveUseCase
from tests.conftest import OUT_OF_SCOPE_VALID_4X4
from tests.entity.conftest import GRID_G3, GRID_STEP_A_SUCCESS


class TestDomainResolverIntegration:
    """End-to-end resolve through Control orchestration."""

    def test_g2_example_returns_reverse_success_solution(self) -> None:
        use_case = ResolveUseCase(domain_resolver=DomainResolver())

        result = use_case.execute(OUT_OF_SCOPE_VALID_4X4)

        assert result == [3, 3, 6, 4, 4, 1]

    def test_step_a_success_grid_returns_small_first_solution(self) -> None:
        use_case = ResolveUseCase(domain_resolver=DomainResolver())

        result = use_case.execute(GRID_STEP_A_SUCCESS)

        assert result == [2, 1, 5, 3, 4, 12]

    def test_g3_returns_no_valid_solution_failure(self) -> None:
        use_case = ResolveUseCase(domain_resolver=DomainResolver())

        result = use_case.execute(GRID_G3)

        assert result.code == NO_VALID_SOLUTION_CODE
