"""Boundary ErrorMapper — E006 NO_VALID_SOLUTION contract (RF-02)."""

from __future__ import annotations

from src.boundary.contracts import (
    NO_VALID_SOLUTION_CODE,
    NO_VALID_SOLUTION_MESSAGE,
    no_valid_solution_failure,
)
from src.boundary.error_mapper import ErrorMapper


class TestErrorMapperE006:
    """E006 mapping via ErrorMapper (RF-02)."""

    def test_map_unsolvable_domain_returns_e006_contract(self) -> None:
        result = ErrorMapper.map_unsolvable_domain()

        assert result.code == NO_VALID_SOLUTION_CODE
        assert result.message == NO_VALID_SOLUTION_MESSAGE

    def test_map_unsolvable_domain_matches_factory(self) -> None:
        assert ErrorMapper.map_unsolvable_domain() == no_valid_solution_failure()
