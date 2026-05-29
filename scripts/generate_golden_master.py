#!/usr/bin/env python3
"""Generate or refresh ``tests/golden_master_expected.txt`` from live solver output.

Usage:
    python scripts/generate_golden_master.py
    python scripts/generate_golden_master.py --check   # compare only, exit 1 on diff
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from magic_square.control.domain_resolver import DomainResolver  # noqa: E402
from magic_square.control.resolve_use_case import ResolveUseCase  # noqa: E402
from tests.helpers.golden_master import (  # noqa: E402
    DEFAULT_GOLDEN_MASTER_PATH,
    approve_golden_master,
    build_golden_document,
)


def main() -> int:
    """Capture solver output and write or verify the golden master baseline."""
    parser = argparse.ArgumentParser(
        description="Generate Magic Square Golden Master baseline (GM-1).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_GOLDEN_MASTER_PATH,
        help="Target baseline file path.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare only; exit 1 when baseline differs (no write).",
    )
    args = parser.parse_args()

    use_case = ResolveUseCase(domain_resolver=DomainResolver())
    actual = build_golden_document(use_case)

    if args.check:
        try:
            status = approve_golden_master(
                actual,
                args.output,
                auto_create=False,
                force_update=False,
            )
        except AssertionError as exc:
            print(exc, file=sys.stderr)
            return 1
        print(f"Golden master OK ({status}): {args.output}")
        return 0

    status = approve_golden_master(
        actual,
        args.output,
        auto_create=True,
        force_update=True,
    )
    print(f"Golden master {status}: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
