"""Golden Master regression tests (GM-2) — Magic Square Solver.

Run subset::

    pytest -m golden_master -v

Approve baseline updates::

    pytest -m golden_master --golden-approve -v
"""

from __future__ import annotations

import pytest

from src.control.domain_resolver import DomainResolver
from src.control.resolve_use_case import ResolveUseCase
from tests.helpers.golden_master import (
    GOLDEN_MASTER_PATH,
    assert_golden_master,
    assert_golden_section,
    assert_scenario_output_contract,
)
from tests.helpers.golden_scenarios import (
    GOLDEN_TEST_CASES,
    scenario_by_section,
)

pytestmark = pytest.mark.golden_master


@pytest.fixture
def resolve_use_case() -> ResolveUseCase:
    """Production wiring: real DomainResolver behind ResolveUseCase."""
    return ResolveUseCase(domain_resolver=DomainResolver())


@pytest.mark.parametrize(
    ("test_case_id", "section_id"),
    GOLDEN_TEST_CASES,
    ids=[tc_id for tc_id, _ in GOLDEN_TEST_CASES],
)
def test_gm_tc_matches_golden_baseline(
    test_case_id: str,
    section_id: str,
    resolve_use_case: ResolveUseCase,
    golden_approve: bool,
) -> None:
    """GM-2 per-scenario golden compare with API result contract checks.

    Covers:
        GM-TC-01: normal combination success
        GM-TC-02: reverse combination success (fallback)
        GM-TC-03: INVALID_BLANK_COUNT
        GM-TC-04: DUPLICATE_NUMBER (``DUPLICATE_NON_ZERO``)
        GM-TC-05: NO_VALID_MAGIC_SQUARE (``NO_VALID_SOLUTION``)
    """
    scenario = scenario_by_section(section_id)
    assert scenario.test_case_id == test_case_id

    assert_golden_section(
        resolve_use_case,
        scenario,
        golden_path=GOLDEN_MASTER_PATH,
        approve=golden_approve,
    )
    assert_scenario_output_contract(resolve_use_case, scenario)


def test_golden_master_document_matches_baseline(
    resolve_use_case: ResolveUseCase,
    golden_approve: bool,
) -> None:
    """GM-1/GM-2: full ``golden_master_expected.txt`` approve/compare."""
    assert_golden_master(
        resolve_use_case,
        golden_path=GOLDEN_MASTER_PATH,
        approve=golden_approve,
    )
