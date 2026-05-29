"""Track A — U-OUT-01~03 (Report/09). Boundary output contract via ResolveUseCase."""

from __future__ import annotations

from src.control.domain_resolver import DomainResolver
from src.control.resolve_use_case import ResolveUseCase
from src.boundary.result_formatter import ResultFormatter
from tests.entity.conftest import GRID_G2


class TestUOut01SuccessPayloadLengthSix:
    """U-OUT-01 — success result length == 6."""

    def test_u_out_01_success_payload_length_is_six(self) -> None:
        use_case = ResolveUseCase(domain_resolver=DomainResolver())

        result = use_case.execute(GRID_G2)

        assert isinstance(result, list)
        assert len(result) == 6


class TestUOut02SuccessCoordinatesOneIndexed:
    """U-OUT-02 — r,c in [1,4] (1-index)."""

    def test_u_out_02_success_coordinates_are_one_indexed(self) -> None:
        use_case = ResolveUseCase(domain_resolver=DomainResolver())

        result = use_case.execute(GRID_G2)

        assert isinstance(result, list)
        assert ResultFormatter.is_valid_solution_format(result)


class TestUOut03SuccessPayloadStructure:
    """U-OUT-03 — success envelope / six int slots contract."""

    def test_u_out_03_success_payload_has_six_integer_slots(self) -> None:
        use_case = ResolveUseCase(domain_resolver=DomainResolver())

        result = use_case.execute(GRID_G2)

        assert result == [3, 3, 6, 4, 4, 1]
