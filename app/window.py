import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, 
    QSplitter, QLabel, QListWidgetItem, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .theory_viewer import TheoryViewer
from .quiz_widget import QuizWidget
from .styles import APP_STYLESHEET, MODULE_INFO, COLORS, apply_matplotlib_dark_theme

# Module directory names (index-aligned with MODULE_INFO)
MODULE_DIRS = [
    "module_00_intro",
    "module_01_camera",
    "module_02_coords",
    "module_03_linalg",
    "module_04_raytracing",
    "module_05_volrend",
    "module_06_mlp",
    "module_07_pe",
    "module_08_pipeline",
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeRF_Edu 🧪 — From Pixels to Neural Radiance Fields")
        self.resize(1500, 950)
        
        # Apply dark theme
        self.setStyleSheet(APP_STYLESHEET)
        apply_matplotlib_dark_theme()
        
        # Track completed modules
        self.completed_modules = set()
        
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Header Bar ──
        header = QWidget()
        header.setFixedHeight(52)
        header.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS["bg_secondary"]}, stop:1 {COLORS["bg_tertiary"]});
                border-bottom: 1px solid {COLORS["border"]};
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        title_label = QLabel("🧪 NeRF_Edu")
        title_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {COLORS["accent_blue"]};
            background: transparent;
            border: none;
        """)
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("From Pixels to Neural Radiance Fields — An Interactive Journey")
        subtitle_label.setStyleSheet(f"""
            font-size: 13px;
            color: {COLORS["text_secondary"]};
            background: transparent;
            border: none;
        """)
        header_layout.addWidget(subtitle_label)
        header_layout.addStretch()
        
        self.progress_label = QLabel("Progress: 0 / 9 modules")
        self.progress_label.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS["accent_teal"]};
            background: transparent;
            border: none;
        """)
        header_layout.addWidget(self.progress_label)
        
        main_layout.addWidget(header)

        # ── Content Area ──
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Splitter for Sidebar, Theory, Interactive
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # ── Sidebar ──
        sidebar_container = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Sidebar header
        sidebar_header = QLabel("  📚 MODULES")
        sidebar_header.setFixedHeight(36)
        sidebar_header.setStyleSheet(f"""
            background-color: {COLORS["bg_secondary"]};
            color: {COLORS["text_secondary"]};
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 2px;
            padding-left: 16px;
            border-bottom: 1px solid {COLORS["border"]};
            border-right: 1px solid {COLORS["border"]};
        """)
        sidebar_layout.addWidget(sidebar_header)
        
        self.sidebar = QListWidget()
        for i, info in enumerate(MODULE_INFO):
            text = f"{info['emoji']}  {info['name']}  {info['difficulty']}"
            item = QListWidgetItem(text)
            self.sidebar.addItem(item)
        
        self.sidebar.currentRowChanged.connect(self.load_module)
        sidebar_layout.addWidget(self.sidebar)
        
        # ── Theory Viewer ──
        self.theory_viewer = TheoryViewer()

        # ── Interactive Widget Container (scrollable) ──
        interactive_scroll = QScrollArea()
        interactive_scroll.setWidgetResizable(True)
        interactive_scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.interactive_container = QWidget()
        self.interactive_layout = QVBoxLayout(self.interactive_container)
        self.interactive_layout.setContentsMargins(8, 8, 8, 8)
        
        interactive_scroll.setWidget(self.interactive_container)

        splitter.addWidget(sidebar_container)
        splitter.addWidget(self.theory_viewer)
        splitter.addWidget(interactive_scroll)

        # Set initial sizes (Sidebar 14%, Theory 40%, Interactive 46%)
        splitter.setSizes([210, 580, 710])

        content_layout.addWidget(splitter)
        main_layout.addWidget(content_widget)
        
        # Load first module by default
        self.sidebar.setCurrentRow(0)

    def _mark_completed(self, index):
        """Mark a module as visited/completed and update progress."""
        self.completed_modules.add(index)
        # Update the sidebar item to show a checkmark
        item = self.sidebar.item(index)
        info = MODULE_INFO[index]
        item.setText(f"✅ {info['emoji']}  {info['name']}")
        # Update progress
        self.progress_label.setText(
            f"Progress: {len(self.completed_modules)} / {len(MODULE_INFO)} modules"
        )

    def _get_theory_path(self, module_dir):
        """Get the theory.md path for a given module directory name."""
        return os.path.join(
            os.path.dirname(__file__), "..", "modules", module_dir, "theory.md"
        )

    def _get_quiz_path(self, module_dir):
        """Get the quiz.json path for a given module directory name."""
        return os.path.join(
            os.path.dirname(__file__), "..", "modules", module_dir, "quiz.json"
        )

    def _add_quiz(self, module_dir):
        """Add a quiz widget for the given module if quiz.json exists."""
        quiz_path = self._get_quiz_path(module_dir)
        if os.path.exists(quiz_path):
            quiz = QuizWidget(quiz_path)
            self.interactive_layout.addWidget(quiz)

    def load_module(self, index):
        # Clear interactive layout
        for i in reversed(range(self.interactive_layout.count())): 
            widget_to_remove = self.interactive_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        if index < 0 or index >= len(MODULE_DIRS):
            return

        module_dir = MODULE_DIRS[index]
        theory_path = self._get_theory_path(module_dir)
        self.theory_viewer.load_markdown(theory_path)
        
        # Mark as completed after visiting
        self._mark_completed(index)

        # Load the corresponding interactive widget
        if index == 0:
            # Module 0: Intro
            from modules.module_00_intro.widget import IntroWidget
            widget = IntroWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
        elif index == 1:
            from modules.module_01_camera.widget import CameraWidget
            widget = CameraWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
        elif index == 2:
            from modules.module_02_coords.widget import CoordinatesWidget
            widget = CoordinatesWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
        elif index == 3:
            from modules.module_03_linalg.widget import LinalgWidget
            widget = LinalgWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
        elif index == 4:
            from modules.module_04_raytracing.widget import RayMarchingWidget
            widget = RayMarchingWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
        elif index == 5:
            from modules.module_05_volrend.widget import VolumeRenderingWidget
            widget = VolumeRenderingWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
        elif index == 6:
            from modules.module_06_mlp.widget import MLPWidget
            widget = MLPWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
        elif index == 7:
            from modules.module_07_pe.widget import PEWidget
            widget = PEWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
        elif index == 8:
            from modules.module_08_pipeline.widget import PipelineWidget
            widget = PipelineWidget()
            self.interactive_layout.addWidget(widget)
            self._add_quiz(module_dir)
