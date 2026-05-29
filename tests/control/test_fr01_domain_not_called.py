"""AC-FR01-01 / AC-FR01-05, PRD §8.1 INVALID_SIZE — Domain resolver isolation."""

from __future__ import annotations

from unittest.mock import create_autospec

import pytest

from src.control.domain_resolver import DomainResolver
from src.control.resolve_use_case import ResolveUseCase
from tests.helpers.fr01_contract import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


class TestInvalidSizeDomainIsolation:
    """AC-FR01-01, PRD §8.1 INVALID_SIZE — resolve() must not run on size failure."""

    def test_none_grid_resolve_called_zero_times_with_mock(
        self,
        grid_none: None,
    ) -> None:
        # AC-FR01-01, AC-FR01-05
        # Given: None grid and autospec DomainResolver mock (spy)
        domain_resolver = create_autospec(DomainResolver, instance=True)
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        # When: execute is invoked
        result = use_case.execute(grid_none)

        # Then: resolve is never called and failure contract is returned
        domain_resolver.resolve.assert_not_called()
        assert domain_resolver.resolve.call_count == 0
        assert result.code == INVALID_SIZE_CODE
        assert result.message == INVALID_SIZE_MESSAGE

    def test_none_grid_boundary_handles_before_resolve(
        self,
        grid_none: None,
    ) -> None:
        # AC-FR01-01, AC-FR01-05
        # Given: None must be rejected before Domain receives grid
        domain_resolver = create_autospec(DomainResolver, instance=True)
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        # When: orchestration runs
        use_case.execute(grid_none)

        # Then: resolve() did not receive None (no direct Domain entry)
        domain_resolver.resolve.assert_not_called()
        for call in domain_resolver.resolve.call_args_list:
            assert call.args[0] is not None


class TestInvalidSizeResolveMockStrictness:
    """AC-FR01-01, PRD §8.1 INVALID_SIZE — mock call is a test failure."""

    def test_resolve_mock_any_call_fails_red_if_invoked(
        self,
        grid_none: None,
    ) -> None:
        # AC-FR01-01, AC-FR01-05
        # Given: strict mock — any resolve() call fails the test
        domain_resolver = create_autospec(DomainResolver, instance=True)

        def fail_on_resolve(*_args: object, **_kwargs: object) -> None:
            pytest.fail("resolve() must not be called when grid=None (AC-FR01-05)")

        domain_resolver.resolve.side_effect = fail_on_resolve
        use_case = ResolveUseCase(domain_resolver=domain_resolver)

        # When: execute with None grid
        use_case.execute(grid_none)

        # Then: side_effect not triggered (assert_not_called as backstop)
        domain_resolver.resolve.assert_not_called()


class TestInvalidSizeDomainScopeLimit:
    """AC-FR01-01 scope — FR-02~05 and AC-FR01-02~05 are out of this RED commit."""

    def test_scope_commit_excludes_fr01_02_through_fr05_cases(self) -> None:
        # AC-FR01-01
        # Given: RED scope is size validation only
        forbidden_case_labels = (
            "blank_count_not_two",
            "value_out_of_range",
            "duplicate_non_zero",
            "blank_finder",
            "missing_number_finder",
            "magic_square_validator",
            "solver_small_first",
            "solver_reverse",
        )

        # When: inspecting this module's test names
        import tests.control.test_fr01_domain_not_called as module_under_test

        collected_names = [
            name
            for name in dir(module_under_test)
            if name.startswith("test_")
        ]

        # Then: no FR-01-02~05 / FR-02~05 scenario tests in this file
        for label in forbidden_case_labels:
            assert not any(label in name for name in collected_names)
