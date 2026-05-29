"""PyQt application bootstrap for Magic Square GUI."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from src.boundary.gui.main_window import MainWindow
from src.boundary.gui.presenter import GridPresenter
from src.control import DomainResolver, ResolveUseCase


def create_main_window() -> MainWindow:
    """Build MainWindow with default Control-layer wiring.

    Returns:
        Configured MainWindow instance.
    """
    use_case = ResolveUseCase(domain_resolver=DomainResolver())
    presenter = GridPresenter(use_case=use_case)
    return MainWindow(presenter=presenter)


def main() -> int:
    """Launch the Magic Square GUI application.

    Returns:
        Process exit code from QApplication.exec().
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Magic Square 4x4")
    app.setOrganizationName("MagicSquare")

    window = create_main_window()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
