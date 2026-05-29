"""PyQt GUI package for Magic Square 4x4."""

from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ["create_main_window", "main"]

if TYPE_CHECKING:
    from src.boundary.gui.app import create_main_window, main


def __getattr__(name: str) -> object:
    if name == "create_main_window":
        from src.boundary.gui.app import create_main_window

        return create_main_window
    if name == "main":
        from src.boundary.gui.app import main

        return main
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
