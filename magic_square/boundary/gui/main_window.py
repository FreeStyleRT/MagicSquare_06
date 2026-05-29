"""Main application window for Magic Square 4x4."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magic_square.boundary.gui.examples import EXAMPLE_GRID_D02
from magic_square.boundary.gui.grid_widget import GridWidget
from magic_square.boundary.gui.presenter import GridPresenter, PresenterOutcome


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
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("Magic Square 4×4")
        self.setMinimumSize(420, 520)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(12)
        root.setContentsMargins(16, 16, 16, 16)

        header = QLabel("4×4 마방진 풀이")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(header)

        root.addWidget(self._grid_widget)

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

        root.addLayout(button_row)

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

        root.addWidget(result_frame)

        self.statusBar().showMessage("격자를 입력한 뒤 [풀이]를 누르세요.")

    def _on_solve(self) -> None:
        grid = self._grid_widget.get_grid()
        outcome = self._presenter.solve(grid)
        self._show_outcome(outcome)

    def _on_load_example(self) -> None:
        self._grid_widget.set_grid(EXAMPLE_GRID_D02)
        self._result_label.setText("예제 격자가 로드되었습니다. [풀이]를 누르세요.")
        self._result_label.setStyleSheet("")
        self.statusBar().showMessage("예제 D-02 격자 로드 완료")

    def _on_clear(self) -> None:
        self._grid_widget.clear()
        self._result_label.setText("격자가 초기화되었습니다.")
        self._result_label.setStyleSheet("")
        self.statusBar().showMessage("격자 초기화 완료")

    def _show_outcome(self, outcome: PresenterOutcome) -> None:
        if outcome.status == "success" and outcome.solution is not None:
            text = self._presenter.format_solution(outcome.solution)
            self._result_label.setText(text)
            self._result_label.setStyleSheet(
                "color: #1b5e20; background: #e8f5e9; padding: 8px; "
                "border-radius: 4px;",
            )
            self.statusBar().showMessage("풀이 성공")
            return

        if outcome.status == "failure" and outcome.failure is not None:
            text = (
                f"오류 코드: {outcome.failure.code}\n"
                f"메시지: {outcome.failure.message}"
            )
            self._result_label.setText(text)
            self._result_label.setStyleSheet(
                "color: #b71c1c; background: #ffebee; padding: 8px; "
                "border-radius: 4px;",
            )
            self.statusBar().showMessage(f"검증 실패 — {outcome.failure.code}")
            return

        message = outcome.error_message or "알 수 없는 오류가 발생했습니다."
        self._result_label.setText(f"처리 불가: {message}")
        self._result_label.setStyleSheet(
            "color: #e65100; background: #fff3e0; padding: 8px; "
            "border-radius: 4px;",
        )
        self.statusBar().showMessage("도메인 로직 미구현 또는 내부 오류")

        if "not implemented" in message.lower():
            QMessageBox.information(
                self,
                "기능 미구현",
                "유효한 4×4 격자는 크기 검증을 통과했습니다.\n"
                "도메인 풀이 로직(FR-02~FR-05)은 아직 구현되지 않았습니다.",
            )
