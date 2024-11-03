"""
Reusable quiz widget for NeRF_Edu modules.
Loads questions from JSON files and provides instant feedback.
"""

import json
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QRadioButton, QButtonGroup, QFrame, QScrollArea, QGroupBox
)
from PyQt6.QtCore import Qt
from app.styles import COLORS


class QuizQuestionWidget(QFrame):
    """A single quiz question with radio-button answers and feedback."""
    
    def __init__(self, question_data, question_number):
        super().__init__()
        self.question_data = question_data
        self.answered = False
        self.correct = False
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS["bg_secondary"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 10px;
                padding: 16px;
                margin: 4px 0;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Question text
        q_label = QLabel(f"Q{question_number}: {question_data['question']}")
        q_label.setWordWrap(True)
        q_label.setStyleSheet(f"""
            font-size: 14px; font-weight: bold; 
            color: {COLORS["text_primary"]};
            border: none; background: transparent;
        """)
        layout.addWidget(q_label)
        
        # Answer options
        self.button_group = QButtonGroup(self)
        self.radio_buttons = []
        
        for i, option in enumerate(question_data["options"]):
            rb = QRadioButton(option)
            rb.setStyleSheet(f"""
                QRadioButton {{
                    color: {COLORS["text_secondary"]};
                    font-size: 13px;
                    spacing: 8px;
                    padding: 6px 4px;
                    border: none; background: transparent;
                }}
                QRadioButton::indicator {{
                    width: 16px; height: 16px;
                    border: 2px solid {COLORS["border"]};
                    border-radius: 9px;
                    background-color: {COLORS["bg_tertiary"]};
                }}
                QRadioButton::indicator:checked {{
                    background-color: {COLORS["accent_blue"]};
                    border-color: {COLORS["accent_blue"]};
                }}
                QRadioButton:hover {{
                    color: {COLORS["text_primary"]};
                }}
            """)
            self.button_group.addButton(rb, i)
            self.radio_buttons.append(rb)
            layout.addWidget(rb)
        
        # Submit button
        self.submit_btn = QPushButton("Check Answer")
        self.submit_btn.setFixedWidth(140)
        self.submit_btn.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_btn)
        
        # Feedback label (hidden initially)
        self.feedback_label = QLabel("")
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setVisible(False)
        self.feedback_label.setStyleSheet(f"""
            border: none; background: transparent;
            padding: 8px; font-size: 13px;
        """)
        layout.addWidget(self.feedback_label)
    
    def check_answer(self):
        if self.answered:
            return
        
        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            return  # nothing selected
        
        self.answered = True
        correct_idx = self.question_data["correct"]
        
        if selected_id == correct_idx:
            self.correct = True
            self.feedback_label.setText(
                f"✅ Correct! {self.question_data.get('explanation', '')}"
            )
            self.feedback_label.setStyleSheet(f"""
                border: none; padding: 10px; font-size: 13px;
                background-color: rgba(63, 185, 80, 0.12);
                color: {COLORS["accent_green"]};
                border-radius: 6px;
            """)
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS["bg_secondary"]};
                    border: 2px solid {COLORS["accent_green"]};
                    border-radius: 10px;
                    padding: 16px;
                    margin: 4px 0;
                }}
            """)
        else:
            self.correct = False
            correct_text = self.question_data["options"][correct_idx]
            self.feedback_label.setText(
                f"❌ Not quite. The correct answer is: **{correct_text}**\n\n"
                f"{self.question_data.get('explanation', '')}"
            )
            self.feedback_label.setStyleSheet(f"""
                border: none; padding: 10px; font-size: 13px;
                background-color: rgba(248, 81, 73, 0.12);
                color: {COLORS["accent_red"]};
                border-radius: 6px;
            """)
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS["bg_secondary"]};
                    border: 2px solid {COLORS["accent_red"]};
                    border-radius: 10px;
                    padding: 16px;
                    margin: 4px 0;
                }}
            """)
        
        self.feedback_label.setVisible(True)
        self.submit_btn.setEnabled(False)
        self.submit_btn.setText("Answered")
        
        # Disable radio buttons
        for rb in self.radio_buttons:
            rb.setEnabled(False)
        
        # Highlight correct answer
        self.radio_buttons[correct_idx].setStyleSheet(f"""
            QRadioButton {{
                color: {COLORS["accent_green"]};
                font-size: 13px; font-weight: bold;
                spacing: 8px; padding: 6px 4px;
                border: none; background: transparent;
            }}
            QRadioButton::indicator {{
                width: 16px; height: 16px;
                border: 2px solid {COLORS["accent_green"]};
                border-radius: 9px;
                background-color: {COLORS["accent_green"] if selected_id == correct_idx else COLORS["bg_tertiary"]};
            }}
        """)


class QuizWidget(QWidget):
    """
    A quiz panel that loads questions from a JSON file.
    
    Expected JSON format:
    {
        "title": "Module 1 Quiz",
        "questions": [
            {
                "question": "What does the focal length control?",
                "options": ["Field of View", "Exposure", "Focus distance", "Aperture"],
                "correct": 0,
                "explanation": "Focal length directly determines the FOV..."
            }
        ]
    }
    """
    
    def __init__(self, quiz_path=None):
        super().__init__()
        self.quiz_data = None
        self.question_widgets = []
        self.setup_ui()
        
        if quiz_path and os.path.exists(quiz_path):
            self.load_quiz(quiz_path)
    
    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 8, 0, 0)
        self.main_layout.setSpacing(8)
        
        # Header
        self.header = QLabel("📝 Knowledge Check")
        self.header.setStyleSheet(f"""
            font-size: 16px; font-weight: bold; 
            color: {COLORS["accent_gold"]};
            padding: 8px 0;
        """)
        self.main_layout.addWidget(self.header)
        
        # Score label
        self.score_label = QLabel("")
        self.score_label.setStyleSheet(f"""
            font-size: 12px; color: {COLORS["text_secondary"]};
        """)
        self.main_layout.addWidget(self.score_label)
        
        # Questions container (scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
        
        self.questions_container = QWidget()
        self.questions_layout = QVBoxLayout(self.questions_container)
        self.questions_layout.setSpacing(12)
        self.questions_layout.addStretch()
        
        scroll.setWidget(self.questions_container)
        self.main_layout.addWidget(scroll)
    
    def load_quiz(self, quiz_path):
        """Load quiz questions from a JSON file."""
        try:
            with open(quiz_path, 'r', encoding='utf-8') as f:
                self.quiz_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.header.setText("📝 Quiz not available")
            return
        
        # Clear existing questions
        self.question_widgets.clear()
        for i in reversed(range(self.questions_layout.count())):
            item = self.questions_layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        
        title = self.quiz_data.get("title", "Knowledge Check")
        self.header.setText(f"📝 {title}")
        
        questions = self.quiz_data.get("questions", [])
        self.score_label.setText(f"0 / {len(questions)} correct")
        
        for idx, q_data in enumerate(questions):
            q_widget = QuizQuestionWidget(q_data, idx + 1)
            q_widget.submit_btn.clicked.connect(self.update_score)
            self.question_widgets.append(q_widget)
            self.questions_layout.insertWidget(idx, q_widget)
    
    def update_score(self):
        """Update the score display after any answer."""
        correct = sum(1 for qw in self.question_widgets if qw.correct)
        total = len(self.question_widgets)
        answered = sum(1 for qw in self.question_widgets if qw.answered)
        
        self.score_label.setText(f"{correct} / {total} correct  ({answered} answered)")
        
        if answered == total:
            if correct == total:
                self.score_label.setStyleSheet(f"""
                    font-size: 14px; font-weight: bold;
                    color: {COLORS["accent_green"]};
                    padding: 4px 0;
                """)
                self.score_label.setText(f"🎉 Perfect Score! {correct}/{total}")
            else:
                self.score_label.setStyleSheet(f"""
                    font-size: 14px; font-weight: bold;
                    color: {COLORS["accent_gold"]};
                    padding: 4px 0;
                """)
                self.score_label.setText(f"Score: {correct}/{total} — Review the marked questions!")
