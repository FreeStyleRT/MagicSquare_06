"""Screen layer tests — ResultPresenter, grid fixtures (RF-06~08)."""

from __future__ import annotations

import importlib.util

import pytest

from src.boundary.contracts import invalid_size_failure
from src.boundary.gui.grid_fixtures import EXAMPLE_GRID, GRID_G1, GRID_G2
from src.boundary.gui.presenter import PresenterOutcome
from src.boundary.gui.result_presenter import ResultPresenter
from tests.entity.conftest import GRID_G1 as ENTITY_GRID_G1
from tests.entity.conftest import GRID_G2 as ENTITY_GRID_G2


class TestGridFixturesSsot:
    """RF-07 — GUI grid fixtures align with Entity test fixtures."""

    def test_grid_g1_matches_entity_fixture(self) -> None:
        assert GRID_G1 == ENTITY_GRID_G1

    def test_grid_g2_matches_entity_fixture(self) -> None:
        assert GRID_G2 == ENTITY_GRID_G2

    def test_example_grid_is_g2(self) -> None:
        assert EXAMPLE_GRID == GRID_G2


class TestResultPresenterFormatSolution:
    """RF-06 — success vector formatting lives in Screen layer."""

    def test_format_solution_uses_one_index_labels(self) -> None:
        text = ResultPresenter.format_solution([3, 3, 6, 4, 4, 1])

        assert "행 3" in text
        assert "열 3" in text
        assert "→ 6" in text
        assert "[3, 3, 6, 4, 4, 1]" in text

    def test_is_valid_solution_rejects_wrong_length(self) -> None:
        assert ResultPresenter.is_valid_solution([1, 2, 3]) is False


class TestResultPresenterFormatOutcome:
    """RF-06 — outcome to ResultDisplay mapping."""

    def test_success_outcome_uses_success_style(self) -> None:
        display = ResultPresenter.format_outcome(
            PresenterOutcome(status="success", solution=[2, 2, 7, 3, 3, 10]),
        )

        assert "행 2" in display.text
        assert "#1b5e20" in display.stylesheet
        assert display.status_message == "풀이 성공"

    def test_failure_outcome_uses_failure_style(self) -> None:
        failure = invalid_size_failure()
        display = ResultPresenter.format_outcome(
            PresenterOutcome(status="failure", failure=failure),
        )

        assert failure.code in display.text
        assert "#b71c1c" in display.stylesheet
        assert failure.code in display.status_message


class TestMainWindowImport:
    """RF-08 — MainWindow importable when PyQt6 is installed."""

    @pytest.mark.skipif(
        importlib.util.find_spec("PyQt6.QtWidgets") is None,
        reason="PyQt6 not installed",
    )
    def test_main_window_class_imports(self) -> None:
        from src.boundary.gui.main_window import MainWindow

        assert MainWindow.__name__ == "MainWindow"
