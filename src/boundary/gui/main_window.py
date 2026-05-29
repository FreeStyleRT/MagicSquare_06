"""Main application window for Magic Square 4x4."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.boundary.gui.examples import EXAMPLE_GRID_D02
from src.boundary.gui.grid_widget import GridWidget
from src.boundary.gui.presenter import GridPresenter, PresenterOutcome
from src.boundary.gui.result_presenter import ResultDisplay, ResultPresenter


class MainWindow(QMainWindow):
    """Primary window — grid editor, solve action, and result display."""

    def __init__(self, presenter: GridPresenter, parent: QWidget | None = None) -> None:
        """Initialize window with injected presenter.

        Args:
            presenter: Boundary presenter wired to ResolveUseCase.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._presenter = presenter
        self._grid_widget = GridWidget()
        self._result_label = QLabel("결과가 여기에 표시됩니다.")
        self._init_ui()

    def _init_ui(self) -> None:
        """Build window chrome, grid, controls, and result panel."""
        self.setWindowTitle("Magic Square 4×4")
        self.setMinimumSize(420, 520)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(12)
        root.setContentsMargins(16, 16, 16, 16)

        root.addWidget(self._init_header())
        root.addWidget(self._grid_widget)
        root.addLayout(self._init_action_buttons())
        root.addWidget(self._init_result_panel())

        self.statusBar().showMessage("격자를 입력한 뒤 [풀이]를 누르세요.")

    def _init_header(self) -> QLabel:
        """Create the window title label."""
        header = QLabel("4×4 마방진 풀이")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return header

    def _init_action_buttons(self) -> QHBoxLayout:
        """Create solve, example, and clear buttons."""
        button_row = QHBoxLayout()
        button_row.setSpacing(8)

        solve_btn = QPushButton("풀이")
        solve_btn.setMinimumHeight(36)
        solve_btn.clicked.connect(self._on_solve)
        button_row.addWidget(solve_btn)

        example_btn = QPushButton("예제 불러오기")
        example_btn.setMinimumHeight(36)
        example_btn.clicked.connect(self._on_load_example)
        button_row.addWidget(example_btn)

        clear_btn = QPushButton("초기화")
        clear_btn.setMinimumHeight(36)
        clear_btn.clicked.connect(self._on_clear)
        button_row.addWidget(clear_btn)

        return button_row

    def _init_result_panel(self) -> QFrame:
        """Create the styled result display frame."""
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.Shape.StyledPanel)
        result_layout = QVBoxLayout(result_frame)

        result_title = QLabel("결과")
        result_title_font = QFont()
        result_title_font.setBold(True)
        result_title.setFont(result_title_font)
        result_layout.addWidget(result_title)

        self._result_label.setWordWrap(True)
        self._result_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
        )
        self._result_label.setMinimumHeight(80)
        result_layout.addWidget(self._result_label)

        return result_frame

    def _on_solve(self) -> None:
        grid = self._grid_widget.get_grid()
        outcome = self._presenter.solve(grid)
        self._show_outcome(outcome)

    def _on_load_example(self) -> None:
        self._grid_widget.set_grid(EXAMPLE_GRID_D02)
        self._apply_result_display(
            ResultDisplay(
                text="예제 격자가 로드되었습니다. [풀이]를 누르세요.",
                stylesheet="",
                status_message="예제 D-02 격자 로드 완료",
            ),
        )

    def _on_clear(self) -> None:
        self._grid_widget.clear()
        self._apply_result_display(
            ResultDisplay(
                text="격자가 초기화되었습니다.",
                stylesheet="",
                status_message="격자 초기화 완료",
            ),
        )

    def _show_outcome(self, outcome: PresenterOutcome) -> None:
        self._apply_result_display(ResultPresenter.format_outcome(outcome))

    def _apply_result_display(self, display: ResultDisplay) -> None:
        """Update result label and status bar from a view model."""
        self._result_label.setText(display.text)
        self._result_label.setStyleSheet(display.stylesheet)
        self.statusBar().showMessage(display.status_message)
