"""Tests for GUI presenter (no Qt dependency)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.boundary.contracts import FailureResponse, invalid_size_failure
from src.boundary.error_codes import (
    INVALID_BLANK_COUNT_CODE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    NO_VALID_SOLUTION_CODE,
)
from src.boundary.gui.presenter import GridPresenter
from src.control.resolve_use_case import ResolveUseCase
from src.control.solution_result import SolutionResult
from tests.entity.conftest import GRID_G3


@pytest.fixture
def presenter() -> GridPresenter:
    use_case = ResolveUseCase(domain_resolver=MagicMock())
    return GridPresenter(use_case=use_case)


class TestGridPresenterFailure:
    def test_invalid_size_returns_failure_outcome(
        self, presenter: GridPresenter,
    ) -> None:
        outcome = presenter.solve(None)

        assert outcome.status == "failure"
        assert outcome.failure == invalid_size_failure()

    def test_failure_carries_contract_fields(
        self, presenter: GridPresenter,
    ) -> None:
        outcome = presenter.solve([])

        assert outcome.failure is not None
        assert outcome.failure.code == INVALID_SIZE_CODE
        assert outcome.failure.message == INVALID_SIZE_MESSAGE


class TestGridPresenterSuccess:
    def test_success_outcome_when_use_case_returns_solution(self) -> None:
        resolver = MagicMock()
        resolver.resolve.return_value = SolutionResult.wrap([3, 3, 6, 4, 4, 1])
        use_case = ResolveUseCase(domain_resolver=resolver)
        presenter = GridPresenter(use_case=use_case)

        grid = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 0, 12],
            [4, 14, 15, 0],
        ]
        outcome = presenter.solve(grid)

        assert outcome.status == "success"
        assert outcome.solution == [3, 3, 6, 4, 4, 1]
        resolver.resolve.assert_called_once_with(grid)


class TestGridPresenterSuccessWithRealResolver:
    def test_g2_example_returns_success_outcome(self) -> None:
        from src.control.domain_resolver import DomainResolver

        use_case = ResolveUseCase(domain_resolver=DomainResolver())
        presenter = GridPresenter(use_case=use_case)
        grid = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 0, 12],
            [4, 14, 15, 0],
        ]

        outcome = presenter.solve(grid)

        assert outcome.status == "success"
        assert outcome.solution == [3, 3, 6, 4, 4, 1]


class TestGridPresenterNoValidSolution:
    def test_g3_returns_failure_outcome(self) -> None:
        from src.control.domain_resolver import DomainResolver

        use_case = ResolveUseCase(domain_resolver=DomainResolver())
        presenter = GridPresenter(use_case=use_case)

        outcome = presenter.solve(GRID_G3)

        assert outcome.status == "failure"
        assert outcome.failure is not None
        assert outcome.failure.code == NO_VALID_SOLUTION_CODE


class TestGridPresenterFr01Failure:
    def test_blank_count_failure_returns_failure_outcome(
        self, presenter: GridPresenter,
    ) -> None:
        grid = [[0] * 4 for _ in range(4)]

        outcome = presenter.solve(grid)

        assert outcome.status == "failure"
        assert outcome.failure is not None
        assert outcome.failure.code == INVALID_BLANK_COUNT_CODE
