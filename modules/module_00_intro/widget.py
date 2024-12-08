import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.styles import COLORS


class PipelineStepWidget(QFrame):
    """A single step in the NeRF pipeline flowchart."""
    
    def __init__(self, emoji, title, subtitle, color):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS["bg_tertiary"]};
                border: 2px solid {color};
                border-radius: 12px;
                padding: 8px;
            }}
            QFrame:hover {{
                background-color: {COLORS["bg_hover"]};
                border-color: {COLORS["accent_teal"]};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        
        emoji_lbl = QLabel(emoji)
        emoji_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emoji_lbl.setStyleSheet(f"font-size: 28px; background: transparent; border: none;")
        layout.addWidget(emoji_lbl)
        
        title_lbl = QLabel(title)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setStyleSheet(f"""
            font-size: 12px; font-weight: bold; 
            color: {COLORS["text_primary"]}; 
            background: transparent; border: none;
        """)
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)
        
        sub_lbl = QLabel(subtitle)
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_lbl.setStyleSheet(f"""
            font-size: 10px; 
            color: {COLORS["text_secondary"]}; 
            background: transparent; border: none;
        """)
        sub_lbl.setWordWrap(True)
        layout.addWidget(sub_lbl)


class ArrowLabel(QLabel):
    """A simple arrow label between pipeline steps."""
    def __init__(self, direction="right"):
        super().__init__("→" if direction == "right" else "↓")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
            font-size: 24px; 
            color: {COLORS["accent_teal"]}; 
            font-weight: bold;
            background: transparent;
        """)


class IntroWidget(QWidget):
    """
    Interactive pipeline flowchart for Module 0.
    Shows the 7-step NeRF pipeline with visual connections.
    """
    
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Title
        title = QLabel("🗺️ The NeRF Pipeline")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 20px; font-weight: bold; 
            color: {COLORS["accent_blue"]};
            padding: 8px;
        """)
        main_layout.addWidget(title)
        
        subtitle = QLabel("Every pixel follows this exact journey — from screen coordinate to final color")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"""
            font-size: 12px; 
            color: {COLORS["text_secondary"]};
            margin-bottom: 12px;
        """)
        main_layout.addWidget(subtitle)
        
        # Pipeline Row 1: Input → Camera → Coords → LinAlg
        row1 = QHBoxLayout()
        row1.setSpacing(4)
        
        steps_row1 = [
            ("🖥️", "Input", "Pixel (u,v)", COLORS["accent_blue"]),
            ("📷", "Camera Math", "Intrinsics K\n→ Ray direction", COLORS["accent_blue"]),
            ("🌍", "Coordinates", "Extrinsics c2w\n→ World-space ray", COLORS["accent_teal"]),
            ("📐", "Linear Algebra", "Matrix transforms\nrotate the ray", COLORS["accent_teal"]),
        ]
        
        for i, (emoji, title, sub, color) in enumerate(steps_row1):
            row1.addWidget(PipelineStepWidget(emoji, title, sub, color))
            if i < len(steps_row1) - 1:
                row1.addWidget(ArrowLabel("right"))
        
        main_layout.addLayout(row1)
        
        # Arrow down
        down_arrow = QLabel("⬇")
        down_arrow.setAlignment(Qt.AlignmentFlag.AlignRight)
        down_arrow.setStyleSheet(f"""
            font-size: 24px; 
            color: {COLORS["accent_teal"]}; 
            padding-right: 40px;
        """)
        main_layout.addWidget(down_arrow)
        
        # Pipeline Row 2: Ray March → PE → MLP → VolRend
        row2 = QHBoxLayout()
        row2.setSpacing(4)
        
        steps_row2 = [
            ("🌫️", "Volume Render", "Beer-Lambert\nα-compositing\n→ Final RGB!", COLORS["accent_gold"]),
            ("🧠", "MLP Query", "8-layer network\n→ σ and (r,g,b)", COLORS["accent_purple"]),
            ("🌊", "Pos. Encoding", "sin/cos projection\n→ High-freq features", COLORS["accent_purple"]),
            ("🔦", "Ray Marching", "Sample N points\nalong the ray", COLORS["accent_gold"]),
        ]
        
        for i, (emoji, title, sub, color) in enumerate(steps_row2):
            row2.addWidget(PipelineStepWidget(emoji, title, sub, color))
            if i < len(steps_row2) - 1:
                row2.addWidget(ArrowLabel("right"))
        
        main_layout.addLayout(row2)
        
        # Stats footer
        main_layout.addSpacing(16)
        
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS["bg_secondary"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        stats_layout = QGridLayout(stats_frame)
        
        stats = [
            ("640,000", "Rays per 800×800 image"),
            ("128", "Samples per ray"),
            ("81,920,000", "MLP queries per frame"),
            ("~30 min", "Training time (original)"),
        ]
        
        for col, (value, label) in enumerate(stats):
            val_lbl = QLabel(value)
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_lbl.setStyleSheet(f"""
                font-size: 22px; font-weight: bold; 
                color: {COLORS["accent_blue"]};
                background: transparent; border: none;
            """)
            stats_layout.addWidget(val_lbl, 0, col)
            
            desc_lbl = QLabel(label)
            desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_lbl.setStyleSheet(f"""
                font-size: 11px; 
                color: {COLORS["text_secondary"]};
                background: transparent; border: none;
            """)
            stats_layout.addWidget(desc_lbl, 1, col)
        
        main_layout.addWidget(stats_frame)
        main_layout.addStretch()
