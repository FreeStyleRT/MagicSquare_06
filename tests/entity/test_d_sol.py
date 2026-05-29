"""Track B — D-SOL-01~04 (FR-05 TwoCellSolver + ResultFormatter)."""

from __future__ import annotations

import pytest

from src.entity.exceptions import UnsolvableDomainError
from src.boundary.result_formatter import ResultFormatter
from src.entity.services.two_cell_solver import TwoCellSolver, solution
from src.entity.value_objects.coordinate import Coordinate
from tests.entity.conftest import GRID_G2, GRID_G3, GRID_STEP_A_SUCCESS


class TestDSol01G1StepASmallFirstSuccess:
    """D-SOL-01 — Step A (small-first) success on dedicated grid."""

    def test_d_sol_01_solution_step_a_success(
        self,
        grid_step_a_success: list[list[int]],
    ) -> None:
        # Given: partial matrix where attempt 1 succeeds
        # When: solution(matrix)
        result = solution(grid_step_a_success)

        # Then: small→first blank, large→second blank
        assert result == [2, 1, 5, 3, 4, 12]


class TestDSol02G2StepBReverseSuccess:
    """D-SOL-02 — G2 Step A fail / Step B reverse success."""

    def test_d_sol_02_solution_g2_step_b_reverse_success(
        self,
        grid_g2: list[list[int]],
    ) -> None:
        # Given: G2 partial matrix (PRD D-02)
        # When: solution(matrix)
        result = solution(grid_g2)

        # Then: reverse attempt succeeds
        assert result == [3, 3, 6, 4, 4, 1]


class TestDSol03G3BothAttemptsUnsolvable:
    """D-SOL-03 — G3 both attempts fail → UnsolvableDomainError."""

    def test_d_sol_03_solution_g3_unsolvable_domain_error(
        self,
        grid_g3: list[list[int]],
    ) -> None:
        # Given: G3 unsolvable partial matrix
        # When: solution(matrix)
        with pytest.raises(UnsolvableDomainError):
            solution(grid_g3)


class TestDSol04SuccessFormatLengthAndOneIndex:
    """D-SOL-04 — success len==6 and coords 1-index in [1,4]."""

    @pytest.mark.parametrize(
        "grid",
        [GRID_STEP_A_SUCCESS, GRID_G2],
        ids=["step_a_success", "g2_reverse"],
    )
    def test_d_sol_04_solution_success_length_six_one_index_coords(
        self,
        grid: list[list[int]],
    ) -> None:
        # Given: solvable matrix
        # When: solution(matrix)
        result = solution(grid)

        # Then: format contract
        assert len(result) == 6
        assert ResultFormatter.is_valid_solution_format(result)


class TestTwoCellSolverBehavior:
    """AC-FR05-01~03 — attempt order and class/function parity."""

    def test_attempt_one_tried_before_attempt_two(self, grid_g2: list[list[int]]) -> None:
        solver = TwoCellSolver()
        blanks = [Coordinate(3, 3), Coordinate(4, 4)]
        small, large = 1, 6

        attempt_one = solver._filled_grid(grid_g2, blanks[0], small, blanks[1], large)
        from src.entity.services.magic_square_validator import is_magic_square

        assert is_magic_square(attempt_one) is False
        assert solution(grid_g2) == [3, 3, 6, 4, 4, 1]

    def test_solver_class_matches_function(
        self,
        grid_step_a_success: list[list[int]],
    ) -> None:
        assert TwoCellSolver().solve(grid_step_a_success) == solution(
            grid_step_a_success,
        )

    def test_g3_raises_unsolvable_domain_error(self) -> None:
        with pytest.raises(UnsolvableDomainError):
            solution(GRID_G3)
