"""Tests for GUI presenter (no Qt dependency)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from magic_square.boundary.contracts import FailureResponse, invalid_size_failure
from magic_square.boundary.gui.presenter import GridPresenter
from magic_square.control.resolve_use_case import ResolveUseCase
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
        assert outcome.failure.code == "INVALID_SIZE"
        assert outcome.failure.message == "Grid must be 4x4."


class TestGridPresenterSuccess:
    def test_success_outcome_when_use_case_returns_solution(self) -> None:
        resolver = MagicMock()
        resolver.resolve.return_value = [3, 3, 6, 4, 4, 1]
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
        from magic_square.control.domain_resolver import DomainResolver

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
        from magic_square.control.domain_resolver import DomainResolver

        use_case = ResolveUseCase(domain_resolver=DomainResolver())
        presenter = GridPresenter(use_case=use_case)

        outcome = presenter.solve(GRID_G3)

        assert outcome.status == "failure"
        assert outcome.failure is not None
        assert outcome.failure.code == "NO_VALID_SOLUTION"


class TestGridPresenterFr01Failure:
    def test_blank_count_failure_returns_failure_outcome(
        self, presenter: GridPresenter,
    ) -> None:
        grid = [[0] * 4 for _ in range(4)]

        outcome = presenter.solve(grid)

        assert outcome.status == "failure"
        assert outcome.failure is not None
        assert outcome.failure.code == "INVALID_BLANK_COUNT"


class TestFormatSolution:
    def test_format_solution_uses_one_index_labels(self) -> None:
        text = GridPresenter.format_solution([3, 3, 6, 4, 4, 1])

        assert "행 3" in text
        assert "열 3" in text
        assert "→ 6" in text
        assert "[3, 3, 6, 4, 4, 1]" in text
