"""SC-CTL-002~003 — Control SolutionResult SSOT and E006 mapping (RF-03)."""

from __future__ import annotations

from src.boundary.contracts import NO_VALID_SOLUTION_CODE
from src.control.domain_resolver import DomainResolver
from src.control.resolve_use_case import ResolveUseCase
from src.control.solution_result import SolutionResult
from src.boundary.result_formatter import ResultFormatter
from tests.conftest import OUT_OF_SCOPE_VALID_4X4
from tests.entity.conftest import GRID_G3, GRID_STEP_A_SUCCESS


class TestScCtl002SolutionResultValues:
    """SC-CTL-002 — success int[6] via SolutionResult.values SSOT."""

    def test_sc_ctl_002_domain_resolver_returns_solution_result(self) -> None:
        resolver = DomainResolver()

        result = resolver.resolve(OUT_OF_SCOPE_VALID_4X4)

        assert isinstance(result, SolutionResult)
        assert len(result.values) == 6

    def test_sc_ctl_002_values_are_one_indexed(self) -> None:
        resolver = DomainResolver()

        result = resolver.resolve(GRID_STEP_A_SUCCESS)

        assert ResultFormatter.is_valid_solution_format(result.to_list())

    def test_sc_ctl_002_use_case_exposes_values_as_list(self) -> None:
        use_case = ResolveUseCase(domain_resolver=DomainResolver())

        result = use_case.execute(GRID_STEP_A_SUCCESS)

        assert result == [2, 1, 5, 3, 4, 12]


class TestScCtl003E006FailureMapping:
    """SC-CTL-003 — G3 unsolvable maps to E006 via ErrorMapper."""

    def test_sc_ctl_003_g3_returns_no_valid_solution(self) -> None:
        use_case = ResolveUseCase(domain_resolver=DomainResolver())

        result = use_case.execute(GRID_G3)

        assert result.code == NO_VALID_SOLUTION_CODE
