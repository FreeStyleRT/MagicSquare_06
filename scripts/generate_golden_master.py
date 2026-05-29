#!/usr/bin/env python3
"""Generate or approve the Golden Master baseline for Magic Square Solver."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from magic_square.control.domain_resolver import DomainResolver
from magic_square.control.resolve_use_case import ResolveUseCase
from tests.helpers.golden_master import (
    GOLDEN_MASTER_PATH,
    assert_golden_master,
    build_golden_document,
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture solver output into tests/golden_master_expected.txt",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Write current solver output to the golden baseline file",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_output",
        help="Print captured document to stdout without writing",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=GOLDEN_MASTER_PATH,
        help=f"Golden file path (default: {GOLDEN_MASTER_PATH})",
    )
    return parser.parse_args()


def main() -> int:
    """Run golden capture and optionally approve the baseline.

    Returns:
        Process exit code (0 on success, 1 on mismatch without approve).
    """
    args = _parse_args()
    use_case = ResolveUseCase(domain_resolver=DomainResolver())
    document = build_golden_document(use_case)

    if args.print_output:
        sys.stdout.write(document)
        return 0

    if args.approve or not args.output.exists():
        args.output.write_text(document, encoding="utf-8")
        action = "approved" if args.approve else "created"
        sys.stdout.write(f"Golden Master {action}: {args.output}\n")
        return 0

    try:
        assert_golden_master(
            use_case,
            golden_path=args.output,
            approve=False,
        )
    except AssertionError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1

    sys.stdout.write(f"Golden Master matches: {args.output}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
