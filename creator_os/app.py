import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


APP_TITLE = "Creator OS"
CONFIG_PATH = Path("Settings") / "config.json"
GEMINI_TEST_PROMPT = "Reply only: OK"


@dataclass
class GeminiStatus:
    status: str = "Disconnected"
    model: str = "gemini-3.5-flash"
    response_time_ms: int | None = None
    requests_today: int = 0
    last_error: str = ""


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {
            "gemini": {
                "api_key": "",
                "model": "gemini-3.5-flash",
                "requests_today": 0,
            }
        }
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"gemini": {"api_key": "", "model": "gemini-3.5-flash", "requests_today": 0}}


def save_config(config: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def run_gemini_connection_test(api_key: str, model: str) -> GeminiStatus:
    if not api_key.strip():
        return GeminiStatus(status="Disconnected", model=model, last_error="API 키가 입력되지 않았습니다.")

    payload = json.dumps({"model": model, "input": GEMINI_TEST_PROMPT}).encode("utf-8")
    request = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/interactions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key.strip(),
        },
        method="POST",
    )

    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read().decode("utf-8", errors="replace")
        elapsed = int((time.perf_counter() - started) * 1000)
        if "OK" in raw.upper():
            return GeminiStatus(status="Connected", model=model, response_time_ms=elapsed)
        return GeminiStatus(
            status="Connected",
            model=model,
            response_time_ms=elapsed,
            last_error="응답은 받았지만 OK 확인 문구가 명확하지 않습니다.",
        )
    except urllib.error.HTTPError as error:
        elapsed = int((time.perf_counter() - started) * 1000)
        detail = error.read().decode("utf-8", errors="replace")[:500]
        if error.code == 429:
            return GeminiStatus(
                status="Rate Limited",
                model=model,
                response_time_ms=elapsed,
                last_error="요청 한도에 걸렸습니다.",
            )
        return GeminiStatus(
            status="Disconnected",
            model=model,
            response_time_ms=elapsed,
            last_error=f"HTTP {error.code}: {detail}",
        )
    except urllib.error.URLError as error:
        return GeminiStatus(status="Offline", model=model, last_error=str(error.reason))
    except TimeoutError:
        return GeminiStatus(status="Offline", model=model, last_error="연결 시간이 초과되었습니다.")
    except OSError as error:
        return GeminiStatus(status="Disconnected", model=model, last_error=str(error))


class StatusPill(QLabel):
    def __init__(self, text: str, tone: str = "neutral") -> None:
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(28)
        self.set_tone(tone)

    def set_tone(self, tone: str) -> None:
        colors = {
            "good": ("#065f46", "#d1fae5", "#a7f3d0"),
            "warn": ("#92400e", "#fef3c7", "#fde68a"),
            "bad": ("#991b1b", "#fee2e2", "#fecaca"),
            "neutral": ("#374151", "#f3f4f6", "#e5e7eb"),
        }
        fg, bg, border = colors.get(tone, colors["neutral"])
        self.setStyleSheet(
            f"color: {fg}; background: {bg}; border: 1px solid {border}; "
            "border-radius: 8px; padding: 4px 10px; font-weight: 700;"
        )


class MetricCard(QFrame):
    def __init__(self, title: str, value: str, note: str = "", tone: str = "neutral") -> None:
        super().__init__()
        self.setObjectName("metricCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        note_label = QLabel(note)
        note_label.setObjectName("cardNote")
        note_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        if note:
            layout.addWidget(note_label)
        layout.addStretch()

        border = {
            "good": "#14b8a6",
            "warn": "#f59e0b",
            "bad": "#ef4444",
            "neutral": "#d1d5db",
        }.get(tone, "#d1d5db")
        self.setStyleSheet(
            f"QFrame#metricCard {{ border: 1px solid {border}; border-radius: 8px; background: white; }}"
        )


class Section(QFrame):
    def __init__(self, title: str, description: str = "") -> None:
        super().__init__()
        self.setObjectName("section")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 14, 16, 14)
        self.layout.setSpacing(10)

        heading = QLabel(title)
        heading.setObjectName("sectionTitle")
        self.layout.addWidget(heading)
        if description:
            body = QLabel(description)
            body.setObjectName("bodyText")
            body.setWordWrap(True)
            self.layout.addWidget(body)


def add_button_row(layout: QVBoxLayout, labels: list[str]) -> None:
    row = QHBoxLayout()
    row.setSpacing(8)
    for label in labels:
        button = QPushButton(label)
        button.setMinimumHeight(36)
        row.addWidget(button)
    row.addStretch()
    layout.addLayout(row)


def gemini_tone(status: str) -> str:
    return {
        "Connected": "good",
        "Rate Limited": "warn",
        "Disconnected": "bad",
        "Offline": "bad",
    }.get(status, "neutral")


def gemini_korean(status: str) -> str:
    return {
        "Connected": "연결됨",
        "Rate Limited": "요청 제한",
        "Disconnected": "연결 안 됨",
        "Offline": "오프라인",
    }.get(status, status)


class DashboardPage(QWidget):
    def __init__(self, open_gemini_dialog) -> None:
        super().__init__()
        self.open_gemini_dialog = open_gemini_dialog
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = QLabel("대시보드")
        title.setObjectName("pageTitle")
        self.gemini_pill = StatusPill("Gemini: 연결 안 됨", "bad")
        gemini_button = QPushButton("Gemini 연결 확인")
        gemini_button.clicked.connect(self.open_gemini_dialog)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.gemini_pill)
        header.addWidget(gemini_button)
        layout.addLayout(header)

        metrics = QGridLayout()
        metrics.setSpacing(12)
        cards = [
            MetricCard("오늘 작업", "0개", "승인 대기와 렌더 대기가 여기에 표시됩니다."),
            MetricCard("휴식형 진행률", "0%", "Somnera / Noctis Atlas"),
            MetricCard("보컬형 진행률", "0%", "Excel 가사 업로드부터 시작"),
            MetricCard("숏츠 대기", "0개", "롱폼에서 파생될 후보"),
            MetricCard("렌더 대기", "0개", "Preview Render 필요"),
            MetricCard("60분 미달", "0개", "보컬형 렌더 차단 항목"),
        ]
        for index, card in enumerate(cards):
            metrics.addWidget(card, index // 3, index % 3)
        layout.addLayout(metrics)

        today = Section("오늘 확인할 항목", "누락 파일, 오류 프로젝트, Gemini 오류, 사용자 승인 대기 항목을 우선 표시합니다.")
        checklist = QListWidget()
        checklist.setObjectName("checklist")
        for item in [
            "승인 대기 항목 없음",
            "렌더 대기 항목 없음",
            "누락 파일 없음",
            "오류 프로젝트 없음",
        ]:
            QListWidgetItem(item, checklist)
        today.layout.addWidget(checklist)
        layout.addWidget(today, 1)

    def update_gemini(self, status: GeminiStatus) -> None:
        self.gemini_pill.setText(f"Gemini: {gemini_korean(status.status)}")
        self.gemini_pill.set_tone(gemini_tone(status.status))


class VocalStudioPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("보컬형 제작")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        row = QGridLayout()
        row.setSpacing(12)
        row.addWidget(MetricCard("목표 시간", "60:00", "60분 미만 렌더 차단", "warn"), 0, 0)
        row.addWidget(MetricCard("선택된 플레이리스트", "00:00", "Winner 선택 전", "bad"), 0, 1)
        row.addWidget(MetricCard("부족 시간", "60:00", "추가 Track 필요", "bad"), 0, 2)
        row.addWidget(MetricCard("Gemini A/B 평가", "대기", "Track 단위로 2개씩 평가"), 1, 0)
        row.addWidget(MetricCard("자막 상태", "미생성", "원본 가사 기반 SRT"), 1, 1)
        row.addWidget(MetricCard("Preflight", "대기", "실패 시 렌더 차단"), 1, 2)
        layout.addLayout(row)

        workflow = Section("60분 플레이리스트 MVP 작업 흐름")
        add_button_row(
            workflow.layout,
            ["프로젝트 생성", "Excel 가사 업로드", "A/B 음원 가져오기", "자동 매칭", "Preview Render"],
        )

        steps = QListWidget()
        steps.setObjectName("checklist")
        for item in [
            "대기 - 프로젝트 생성",
            "대기 - Excel 가사 업로드",
            "대기 - A/B 음원 Drag & Drop Import",
            "대기 - Track01 기준 자동 매칭",
            "대기 - Python 길이 분석",
            "대기 - Gemini A/B 평가",
            "대기 - Winner 자동 선택",
            "대기 - 총 길이 60분 검증",
            "대기 - 10초 Preview Render",
        ]:
            QListWidgetItem(item, steps)
        workflow.layout.addWidget(steps)
        layout.addWidget(workflow, 1)


class RestStudioPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        heading = QLabel("휴식형 제작")
        heading.setObjectName("pageTitle")
        layout.addWidget(heading)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(MetricCard("Somnera", "Room Profile", "한 영상 = 하나의 방"), 0, 0)
        grid.addWidget(MetricCard("Noctis Atlas", "Journey Profile", "한 영상 = 하나의 여정"), 0, 1)
        grid.addWidget(MetricCard("Master Playlist", "50~70분", "목표 시간까지 자연스럽게 Loop"), 0, 2)
        layout.addLayout(grid)

        section = Section("제작 흐름", "음악, Ambient Profile, 이미지, Flow Loop 영상을 등록하고 목표 길이만큼 반복 렌더합니다.")
        add_button_row(section.layout, ["프로젝트 생성", "Profile 선택", "Ambient 적용", "Loop 계산", "Render Preview"])
        layout.addWidget(section, 1)


class ShortsStudioPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        heading = QLabel("숏츠 제작")
        heading.setObjectName("pageTitle")
        layout.addWidget(heading)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(MetricCard("포맷", "9:16", "세로 영상"), 0, 0)
        grid.addWidget(MetricCard("후보 길이", "20 / 30 / 45 / 60초", "Hook Finder 기준"), 0, 1)
        grid.addWidget(MetricCard("롱폼 연결", "필수", "Derived Content"), 0, 2)
        layout.addLayout(grid)

        section = Section("Hook Finder", "Python은 에너지 피크와 후렴 후보를 찾고, Gemini는 감정/가사/숏츠 적합성을 평가합니다.")
        add_button_row(section.layout, ["Long Video 선택", "Hook 추출", "Gemini 평가", "세로 렌더", "업로드 준비"])
        layout.addWidget(section, 1)


class LibraryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        heading = QLabel("라이브러리")
        heading.setObjectName("pageTitle")
        layout.addWidget(heading)

        grid = QGridLayout()
        grid.setSpacing(12)
        for index, name in enumerate(["Audio", "Lyrics", "Images", "Videos", "Ambient", "Fonts", "Logos", "Prompts", "Templates"]):
            grid.addWidget(MetricCard(name, "0개", "등록 대기"), index // 3, index % 3)
        layout.addLayout(grid)
        layout.addStretch()


class AnalyticsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        heading = QLabel("분석")
        heading.setObjectName("pageTitle")
        layout.addWidget(heading)

        section = Section("Creator OS Memory", "조회수, CTR, 평균 시청 지속 시간, 좋아요, 댓글, Shorts 성과를 저장하고 다음 제작 방향을 추천합니다.")
        add_button_row(section.layout, ["성과 가져오기", "성공 패턴 보기", "주간 리포트", "월간 리포트"])
        layout.addWidget(section)
        layout.addStretch()


class SettingsPage(QWidget):
    def __init__(self, open_gemini_dialog) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        heading = QLabel("설정")
        heading.setObjectName("pageTitle")
        layout.addWidget(heading)

        gemini = Section("Gemini API", "API 키와 모델을 입력하고 연결 상태를 확인합니다.")
        gemini_button = QPushButton("Gemini API 입력 및 연결 확인")
        gemini_button.setMinimumHeight(40)
        gemini_button.clicked.connect(open_gemini_dialog)
        gemini.layout.addWidget(gemini_button)
        layout.addWidget(gemini)

        paths = Section("작업 폴더", "Original / Working / Render / Export 구조로 원본을 보호합니다.")
        add_button_row(paths.layout, ["CreatorOS 폴더 선택", "로그 폴더 열기", "FFmpeg 경로 설정"])
        layout.addWidget(paths)
        layout.addStretch()


class GeminiDialog(QDialog):
    def __init__(self, config: dict, current_status: GeminiStatus, parent=None) -> None:
        super().__init__(parent)
        self.config = config
        self.result_status = current_status
        self.setWindowTitle("Gemini API 연결 확인")
        self.setMinimumWidth(560)

        gemini_config = self.config.setdefault("gemini", {})

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Gemini API 설정")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        info = QLabel("프로그램 실행 테스트 프롬프트: Reply only: OK")
        info.setObjectName("bodyText")
        layout.addWidget(info)

        self.api_key = QLineEdit(gemini_config.get("api_key", ""))
        self.api_key.setEchoMode(QLineEdit.Password)
        self.api_key.setPlaceholderText("Gemini API Key 입력")
        layout.addWidget(QLabel("API Key"))
        layout.addWidget(self.api_key)

        self.model = QComboBox()
        self.model.addItems(["gemini-3.5-flash", "gemini-3.1-flash", "gemini-3.1-pro", "gemini-2.5-flash"])
        selected_model = gemini_config.get("model", current_status.model)
        index = self.model.findText(selected_model)
        if index >= 0:
            self.model.setCurrentIndex(index)
        layout.addWidget(QLabel("Model"))
        layout.addWidget(self.model)

        self.status_label = QLabel()
        self.status_label.setObjectName("bodyText")
        layout.addWidget(self.status_label)

        self.error_box = QTextEdit()
        self.error_box.setReadOnly(True)
        self.error_box.setFixedHeight(100)
        layout.addWidget(self.error_box)

        buttons = QHBoxLayout()
        test_button = QPushButton("연결 확인")
        save_button = QPushButton("저장")
        close_button = QPushButton("닫기")
        test_button.clicked.connect(self.test_connection)
        save_button.clicked.connect(self.save_settings)
        close_button.clicked.connect(self.accept)
        buttons.addWidget(test_button)
        buttons.addWidget(save_button)
        buttons.addStretch()
        buttons.addWidget(close_button)
        layout.addLayout(buttons)

        self.update_status(current_status)

    def save_settings(self) -> None:
        gemini = self.config.setdefault("gemini", {})
        gemini["api_key"] = self.api_key.text().strip()
        gemini["model"] = self.model.currentText()
        gemini.setdefault("requests_today", 0)
        save_config(self.config)
        QMessageBox.information(self, "저장 완료", "Gemini API 설정을 저장했습니다.")

    def test_connection(self) -> None:
        self.save_settings()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()
        try:
            status = run_gemini_connection_test(self.api_key.text(), self.model.currentText())
        finally:
            QApplication.restoreOverrideCursor()

        if status.status in {"Connected", "Rate Limited"}:
            gemini = self.config.setdefault("gemini", {})
            gemini["requests_today"] = int(gemini.get("requests_today", 0)) + 1
            status.requests_today = gemini["requests_today"]
            save_config(self.config)
        else:
            status.requests_today = int(self.config.setdefault("gemini", {}).get("requests_today", 0))

        self.result_status = status
        self.update_status(status)

    def update_status(self, status: GeminiStatus) -> None:
        response_time = "-" if status.response_time_ms is None else f"{status.response_time_ms} ms"
        self.status_label.setText(
            f"상태: {gemini_korean(status.status)}\n"
            f"Model: {status.model}\n"
            f"Response Time: {response_time}\n"
            f"Requests Today: {status.requests_today}"
        )
        self.error_box.setPlainText(status.last_error or "Last Error: 없음")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.config = load_config()
        gemini_config = self.config.setdefault("gemini", {})
        self.gemini_status = GeminiStatus(
            model=gemini_config.get("model", "gemini-3.5-flash"),
            requests_today=int(gemini_config.get("requests_today", 0)),
        )

        self.setWindowTitle(APP_TITLE)
        self.resize(1240, 800)

        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 16, 14, 14)
        sidebar_layout.setSpacing(12)
        sidebar.setFixedWidth(240)

        brand = QLabel("Creator OS")
        brand.setObjectName("brand")
        subtitle = QLabel("AI 음악 채널 운영체제")
        subtitle.setObjectName("sidebarSub")
        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(subtitle)

        self.nav = QListWidget()
        self.nav.setObjectName("nav")
        sidebar_layout.addWidget(self.nav, 1)

        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage(self.open_gemini_dialog)
        pages = [
            ("대시보드", self.dashboard_page),
            ("보컬형 제작", VocalStudioPage()),
            ("휴식형 제작", RestStudioPage()),
            ("숏츠 제작", ShortsStudioPage()),
            ("라이브러리", LibraryPage()),
            ("분석", AnalyticsPage()),
            ("설정", SettingsPage(self.open_gemini_dialog)),
        ]
        for name, page in pages:
            self.nav.addItem(name)
            self.stack.addWidget(page)

        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.stack, 1)
        self.setCentralWidget(root)

        gemini_action = QAction("Gemini 연결 확인", self)
        gemini_action.triggered.connect(self.open_gemini_dialog)
        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu = self.menuBar().addMenu("파일")
        file_menu.addAction(gemini_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        self.statusBar().showMessage("Creator OS 테스트 셸 준비 완료")
        self.dashboard_page.update_gemini(self.gemini_status)
        self.setStyleSheet(APP_STYLES)

    def open_gemini_dialog(self) -> None:
        dialog = GeminiDialog(self.config, self.gemini_status, self)
        dialog.exec()
        self.gemini_status = dialog.result_status
        self.dashboard_page.update_gemini(self.gemini_status)
        status_text = gemini_korean(self.gemini_status.status)
        self.statusBar().showMessage(f"Gemini 상태: {status_text}")


APP_STYLES = """
QMainWindow { background: #f5f7fb; }
QWidget#sidebar {
    background: #101828;
    color: #e5e7eb;
}
QLabel#brand {
    color: white;
    font-size: 22px;
    font-weight: 800;
}
QLabel#sidebarSub {
    color: #9ca3af;
    font-size: 12px;
}
QListWidget#nav {
    background: transparent;
    color: #d1d5db;
    border: none;
    font-size: 14px;
    outline: none;
}
QListWidget#nav::item {
    min-height: 40px;
    padding: 8px 10px;
    border-radius: 6px;
}
QListWidget#nav::item:selected {
    background: #2563eb;
    color: white;
}
QListWidget#nav::item:hover {
    background: #1f2937;
}
QLabel#pageTitle {
    font-size: 28px;
    font-weight: 800;
    color: #111827;
}
QLabel#dialogTitle {
    font-size: 22px;
    font-weight: 800;
    color: #111827;
}
QLabel#sectionTitle {
    color: #111827;
    font-size: 16px;
    font-weight: 800;
}
QLabel#bodyText {
    font-size: 13px;
    color: #4b5563;
}
QLabel#cardTitle {
    color: #6b7280;
    font-size: 12px;
    font-weight: 700;
}
QLabel#cardValue {
    color: #111827;
    font-size: 24px;
    font-weight: 800;
}
QLabel#cardNote {
    color: #6b7280;
    font-size: 12px;
}
QFrame#section {
    background: white;
    border: 1px solid #dbe1ea;
    border-radius: 8px;
}
QPushButton {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-weight: 700;
}
QPushButton:hover { background: #1d4ed8; }
QLineEdit, QComboBox, QTextEdit {
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px;
    color: #111827;
}
QListWidget#checklist {
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 8px;
    color: #111827;
}
QListWidget#checklist::item {
    min-height: 30px;
}
QMenuBar {
    background: #ffffff;
    color: #111827;
}
QStatusBar {
    background: #ffffff;
    color: #374151;
}
"""


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
