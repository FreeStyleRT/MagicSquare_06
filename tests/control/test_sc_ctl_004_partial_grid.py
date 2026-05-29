"""SC-CTL-004 — locate/find SSOT via PartialGridContext (RF-04)."""

from __future__ import annotations

from src.control.domain_resolver import DomainResolver
from src.entity.services.empty_cell_locator import find_blank_coords
from src.entity.services.missing_number_finder import find_not_exist_nums
from tests.entity.conftest import GRID_G1, GRID_G2


class TestScCtl004PartialGridAnalysis:
    """SC-CTL-004 — single scan context matches FR-02/FR-03 entry points."""

    def test_sc_ctl_004_analyze_matches_find_blank_coords_g1(self) -> None:
        resolver = DomainResolver()

        context = resolver.analyze(GRID_G1)

        assert list(context.blanks) == find_blank_coords(GRID_G1)

    def test_sc_ctl_004_analyze_matches_find_not_exist_nums_g1(self) -> None:
        resolver = DomainResolver()

        context = resolver.analyze(GRID_G1)

        assert list(context.missing) == find_not_exist_nums(GRID_G1)

    def test_sc_ctl_004_analyze_matches_g2_locate_and_find(self) -> None:
        resolver = DomainResolver()

        context = resolver.analyze(GRID_G2)

        assert list(context.blanks) == find_blank_coords(GRID_G2)
        assert list(context.missing) == find_not_exist_nums(GRID_G2)
