"""Golden Master regression tests (GM-1) — approve pattern."""

from __future__ import annotations

import pytest

from magic_square.control.domain_resolver import DomainResolver
from magic_square.control.resolve_use_case import ResolveUseCase
from tests.helpers.golden_master import GOLDEN_MASTER_PATH, assert_golden_master


@pytest.fixture
def resolve_use_case() -> ResolveUseCase:
    """Production wiring: real DomainResolver behind ResolveUseCase."""
    return ResolveUseCase(domain_resolver=DomainResolver())


def test_golden_master_matches_solver_output(
    resolve_use_case: ResolveUseCase,
    golden_approve: bool,
) -> None:
    """GM-1: compare solver output against committed golden baseline."""
    assert_golden_master(
        resolve_use_case,
        golden_path=GOLDEN_MASTER_PATH,
        approve=golden_approve,
    )
