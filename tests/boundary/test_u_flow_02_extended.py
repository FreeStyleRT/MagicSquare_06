"""Track A — U-FLOW-02: invalid FR-01 input must not call Domain resolve."""

from __future__ import annotations

from unittest.mock import create_autospec

import pytest

from src.control.domain_resolver import DomainResolver
from src.control.resolve_use_case import ResolveUseCase
from tests.conftest import (
    GRID_DUPLICATE_NON_ZERO,
    GRID_THREE_BLANKS,
    GRID_VALUE_ABOVE_RANGE,
    GRID_ZERO_BLANKS,
)
from tests.helpers.fr01_contract import (
    DUPLICATE_NON_ZERO_CODE,
    INVALID_BLANK_COUNT_CODE,
    INVALID_SIZE_CODE,
    INVALID_VALUE_RANGE_CODE,
)


class TestUFlow02InvalidInputNeverCallsExecute:
    """U-FLOW-02 / AC-FR01-05 — invalid input → resolve call_count == 0."""

    def test_u_flow_02_null_matrix_execute_not_called(
        self,
        grid_none: None,
    ) -> None:
        # Given: matrix = None
        domain_resolver = create_autospec(DomainResolver, instance=True)
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        # When: execute is invoked
        result = use_case.execute(grid_none)

        # Then: resolve not called
        domain_resolver.resolve.assert_not_called()
        assert result.code == INVALID_SIZE_CODE

    def test_u_flow_02_invalid_size_execute_not_called(self) -> None:
        # Given: 3x4 grid
        domain_resolver = create_autospec(DomainResolver, instance=True)
        use_case = ResolveUseCase(domain_resolver=domain_resolver)
        matrix: list[list[int]] = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

        # When: execute is invoked
        result = use_case.execute(matrix)

        # Then: resolve not called
        domain_resolver.resolve.assert_not_called()
        assert result.code == INVALID_SIZE_CODE

    def test_u_flow_02_invalid_blank_count_execute_not_called(self) -> None:
        # Given: blank count != 2
        domain_resolver = create_autospec(DomainResolver, instance=True)
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        # When: execute is invoked
        result = use_case.execute(GRID_ZERO_BLANKS)

        # Then: resolve not called
        domain_resolver.resolve.assert_not_called()
        assert result.code == INVALID_BLANK_COUNT_CODE

    def test_u_flow_02_invalid_range_execute_not_called(self) -> None:
        # Given: out-of-range value
        domain_resolver = create_autospec(DomainResolver, instance=True)
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        # When: execute is invoked
        result = use_case.execute(GRID_VALUE_ABOVE_RANGE)

        # Then: resolve not called
        domain_resolver.resolve.assert_not_called()
        assert result.code == INVALID_VALUE_RANGE_CODE

    def test_u_flow_02_duplicate_nonzero_execute_not_called(self) -> None:
        # Given: duplicate non-zero
        domain_resolver = create_autospec(DomainResolver, instance=True)
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        # When: execute is invoked
        result = use_case.execute(GRID_DUPLICATE_NON_ZERO)

        # Then: resolve not called
        domain_resolver.resolve.assert_not_called()
        assert result.code == DUPLICATE_NON_ZERO_CODE

    def test_u_flow_02_three_blanks_execute_not_called(self) -> None:
        domain_resolver = create_autospec(DomainResolver, instance=True)
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        use_case.execute(GRID_THREE_BLANKS)

        domain_resolver.resolve.assert_not_called()


class TestUFlow02ResolveMockStrictness:
    """Strict mock — any resolve() call on FR-01 failure fails the test."""

    @pytest.mark.parametrize(
        "grid",
        [GRID_ZERO_BLANKS, GRID_VALUE_ABOVE_RANGE, GRID_DUPLICATE_NON_ZERO],
        ids=["blank_count", "range", "duplicate"],
    )
    def test_resolve_mock_fails_if_invoked_on_fr01_failure(
        self,
        grid: list[list[int]],
    ) -> None:
        domain_resolver = create_autospec(DomainResolver, instance=True)

        def fail_on_resolve(*_args: object, **_kwargs: object) -> None:
            pytest.fail("resolve() must not be called on FR-01 validation failure")

        domain_resolver.resolve.side_effect = fail_on_resolve
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        use_case.execute(grid)

        domain_resolver.resolve.assert_not_called()
