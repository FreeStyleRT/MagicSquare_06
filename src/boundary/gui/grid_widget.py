"""4x4 grid editor widget for Magic Square input."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QSpinBox, QVBoxLayout, QWidget

from src.boundary.gui.constants import (
    BLANK_VALUE,
    CELL_MAX_VALUE,
    CELL_MIN_VALUE,
    GRID_DIMENSION,
)


class GridWidget(QWidget):
    """Editable 4x4 integer grid (0 = blank, 1–16 = filled)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Build the spin-box grid layout.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._cells: list[list[QSpinBox]] = []
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("4×4 격자 (0 = 빈칸, 1–16 = 숫자)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(6)

        for row in range(GRID_DIMENSION):
            row_cells: list[QSpinBox] = []
            for col in range(GRID_DIMENSION):
                spin = QSpinBox()
                spin.setRange(CELL_MIN_VALUE, CELL_MAX_VALUE)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin.setMinimumWidth(56)
                spin.setSpecialValueText("빈칸")
                spin.setValue(BLANK_VALUE)
                grid_layout.addWidget(spin, row, col)
                row_cells.append(spin)
            self._cells.append(row_cells)

        layout.addLayout(grid_layout)

    def get_grid(self) -> list[list[int]]:
        """Read current cell values as a 4x4 matrix.

        Returns:
            Integer matrix matching ResolveUseCase input contract.
        """
        return [
            [self._cells[row][col].value() for col in range(GRID_DIMENSION)]
            for row in range(GRID_DIMENSION)
        ]

    def set_grid(self, grid: list[list[int]]) -> None:
        """Populate cells from a 4x4 matrix.

        Args:
            grid: Source matrix; must be GRID_DIMENSION × GRID_DIMENSION.
        """
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                self._cells[row][col].setValue(grid[row][col])

    def clear(self) -> None:
        """Reset all cells to blank (0)."""
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                self._cells[row][col].setValue(BLANK_VALUE)
