"""
Centralized Dark Theme Stylesheet for NeRF_Edu.
Inspired by 3Blue1Brown's deep navy/teal palette with modern accents.
"""

# ─── Color Palette ─────────────────────────────────────────────────────
COLORS = {
    "bg_primary":    "#0d1117",    # Deep dark (GitHub dark)
    "bg_secondary":  "#161b22",    # Slightly lighter panel
    "bg_tertiary":   "#1c2333",    # Card/group background
    "bg_hover":      "#21262d",    # Hover state
    "bg_selected":   "#1f6feb33",  # Selected item (semi-transparent blue)
    
    "text_primary":  "#e6edf3",    # Main text
    "text_secondary":"#8b949e",    # Muted text
    "text_accent":   "#58a6ff",    # Links / highlights
    
    "accent_blue":   "#58a6ff",    # Primary accent (3B1B inspired)
    "accent_teal":   "#3fb9a2",    # Secondary accent
    "accent_gold":   "#e3b341",    # Warning / highlights  
    "accent_purple": "#bc8cff",    # Tertiary accent
    "accent_red":    "#f85149",    # Error / important
    "accent_green":  "#3fb950",    # Success / completed
    
    "border":        "#30363d",    # Subtle borders
    "border_focus":  "#58a6ff",    # Focus ring
    
    "scrollbar_bg":  "#161b22",
    "scrollbar_fg":  "#30363d",
}

# ─── Module Metadata ───────────────────────────────────────────────────
MODULE_INFO = [
    {"emoji": "🚀", "name": "What is NeRF?",              "difficulty": "⭐",      "short": "Intro"},
    {"emoji": "📷", "name": "How Images are Formed",       "difficulty": "⭐",      "short": "Camera"},
    {"emoji": "🌍", "name": "Coordinate Systems",          "difficulty": "⭐",      "short": "Coords"},
    {"emoji": "📐", "name": "Linear Algebra",              "difficulty": "⭐⭐",    "short": "LinAlg"},
    {"emoji": "🔦", "name": "Ray Tracing & Sampling",      "difficulty": "⭐⭐",    "short": "Rays"},
    {"emoji": "🌫️", "name": "Volume Rendering",            "difficulty": "⭐⭐⭐",  "short": "VolRend"},
    {"emoji": "🧠", "name": "Multi-Layer Perceptrons",     "difficulty": "⭐⭐",    "short": "MLP"},
    {"emoji": "🌊", "name": "Positional Encoding",         "difficulty": "⭐⭐⭐",  "short": "PE"},
    {"emoji": "🎯", "name": "The Full Pipeline",           "difficulty": "⭐⭐⭐",  "short": "Pipeline"},
]

# ─── Main Application Stylesheet ──────────────────────────────────────
APP_STYLESHEET = f"""
/* ── Global ── */
QMainWindow, QWidget {{
    background-color: {COLORS["bg_primary"]};
    color: {COLORS["text_primary"]};
    font-family: 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
}}

/* ── Splitter ── */
QSplitter::handle {{
    background-color: {COLORS["border"]};
    width: 2px;
}}
QSplitter::handle:hover {{
    background-color: {COLORS["accent_blue"]};
}}

/* ── Sidebar List Widget ── */
QListWidget {{
    background-color: {COLORS["bg_secondary"]};
    border: none;
    border-right: 1px solid {COLORS["border"]};
    outline: none;
    padding: 8px 0;
    font-size: 13px;
}}
QListWidget::item {{
    padding: 12px 16px;
    border-left: 3px solid transparent;
    border-bottom: 1px solid {COLORS["border"]};
    color: {COLORS["text_secondary"]};
    min-height: 20px;
}}
QListWidget::item:hover {{
    background-color: {COLORS["bg_hover"]};
    color: {COLORS["text_primary"]};
    border-left: 3px solid {COLORS["accent_teal"]};
}}
QListWidget::item:selected {{
    background-color: {COLORS["bg_selected"]};
    color: {COLORS["accent_blue"]};
    border-left: 3px solid {COLORS["accent_blue"]};
    font-weight: bold;
}}

/* ── Group Boxes ── */
QGroupBox {{
    background-color: {COLORS["bg_tertiary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px;
    padding-top: 28px;
    font-weight: bold;
    color: {COLORS["accent_teal"]};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    background-color: {COLORS["bg_tertiary"]};
    border-radius: 4px;
    color: {COLORS["accent_teal"]};
    font-size: 13px;
}}

/* ── Labels ── */
QLabel {{
    color: {COLORS["text_secondary"]};
    font-size: 13px;
}}

/* ── Sliders ── */
QSlider::groove:horizontal {{
    background-color: {COLORS["bg_hover"]};
    height: 6px;
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background-color: {COLORS["accent_blue"]};
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}}
QSlider::handle:horizontal:hover {{
    background-color: {COLORS["accent_teal"]};
}}
QSlider::sub-page:horizontal {{
    background-color: {COLORS["accent_blue"]};
    border-radius: 3px;
}}

/* ── Buttons ── */
QPushButton {{
    background-color: {COLORS["bg_tertiary"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {COLORS["accent_blue"]};
    color: #ffffff;
    border-color: {COLORS["accent_blue"]};
}}
QPushButton:pressed {{
    background-color: {COLORS["accent_teal"]};
}}
QPushButton:disabled {{
    background-color: {COLORS["bg_hover"]};
    color: {COLORS["text_secondary"]};
    border-color: {COLORS["border"]};
}}

/* ── Checkboxes ── */
QCheckBox {{
    color: {COLORS["text_secondary"]};
    spacing: 8px;
    font-size: 13px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS["border"]};
    border-radius: 4px;
    background-color: {COLORS["bg_tertiary"]};
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS["accent_blue"]};
    border-color: {COLORS["accent_blue"]};
}}
QCheckBox::indicator:hover {{
    border-color: {COLORS["accent_teal"]};
}}

/* ── Progress Bar ── */
QProgressBar {{
    background-color: {COLORS["bg_hover"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 6px;
    text-align: center;
    height: 20px;
    color: {COLORS["text_primary"]};
    font-size: 12px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS["accent_blue"]}, stop:1 {COLORS["accent_teal"]});
    border-radius: 5px;
}}

/* ── Scroll Bars ── */
QScrollBar:vertical {{
    background-color: {COLORS["scrollbar_bg"]};
    width: 10px;
    border: none;
}}
QScrollBar::handle:vertical {{
    background-color: {COLORS["scrollbar_fg"]};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {COLORS["text_secondary"]};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background-color: {COLORS["scrollbar_bg"]};
    height: 10px;
    border: none;
}}
QScrollBar::handle:horizontal {{
    background-color: {COLORS["scrollbar_fg"]};
    border-radius: 5px;
    min-width: 30px;
}}
"""

# ─── Matplotlib Dark Theme Config ──────────────────────────────────────
def apply_matplotlib_dark_theme():
    """Call this once at app startup to set matplotlib's default theme."""
    import matplotlib.pyplot as plt
    
    plt.rcParams.update({
        "figure.facecolor":  COLORS["bg_tertiary"],
        "axes.facecolor":    COLORS["bg_secondary"],
        "axes.edgecolor":    COLORS["border"],
        "axes.labelcolor":   COLORS["text_secondary"],
        "text.color":        COLORS["text_primary"],
        "xtick.color":       COLORS["text_secondary"],
        "ytick.color":       COLORS["text_secondary"],
        "grid.color":        COLORS["border"],
        "legend.facecolor":  COLORS["bg_tertiary"],
        "legend.edgecolor":  COLORS["border"],
        "legend.labelcolor": COLORS["text_primary"],
        "figure.edgecolor":  COLORS["bg_tertiary"],
        "savefig.facecolor": COLORS["bg_tertiary"],
        "lines.linewidth":   2.0,
        "font.size":         11,
        "axes.titlesize":    13,
        "axes.labelsize":    11,
    })


# ─── Theory Viewer HTML Template ───────────────────────────────────────
THEORY_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script>
    MathJax = {{
        tex: {{ inlineMath: [['$','$'], ['\\\\(','\\\\)']], displayMath: [['$$','$$'], ['\\\\[','\\\\]']] }},
        svg: {{ fontCache: 'global' }}
    }};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    
    body {{ 
        background-color: {bg_primary};
        color: {text_primary};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 15px;
        line-height: 1.75;
        padding: 32px 28px;
        -webkit-font-smoothing: antialiased;
    }}
    
    /* ── Typography ── */
    h1 {{
        color: {accent_blue};
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 8px;
        padding-bottom: 12px;
        border-bottom: 2px solid {border};
        letter-spacing: -0.5px;
    }}
    h2 {{
        color: {accent_teal};
        font-size: 20px;
        font-weight: 600;
        margin-top: 36px;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 1px solid {border};
    }}
    h3 {{
        color: {accent_purple};
        font-size: 17px;
        font-weight: 600;
        margin-top: 24px;
        margin-bottom: 8px;
    }}
    p {{
        margin-bottom: 14px;
    }}
    strong {{
        color: {accent_gold};
        font-weight: 600;
    }}
    em {{
        color: {text_secondary};
        font-style: italic;
    }}
    
    /* ── Lists ── */
    ul, ol {{
        margin-left: 24px;
        margin-bottom: 14px;
    }}
    li {{
        margin-bottom: 6px;
    }}
    
    /* ── Code ── */
    code {{
        background-color: {bg_tertiary};
        color: {accent_teal};
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', 'SF Mono', monospace;
        font-size: 13px;
        border: 1px solid {border};
    }}
    pre {{
        background-color: {bg_secondary};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 16px 20px;
        overflow-x: auto;
        margin: 16px 0;
        line-height: 1.5;
    }}
    pre code {{
        background: none;
        border: none;
        padding: 0;
        color: {text_primary};
        font-size: 13px;
    }}
    
    /* ── Blockquotes ── */
    blockquote {{
        border-left: 4px solid {accent_blue};
        margin: 16px 0;
        padding: 12px 20px;
        background-color: {bg_secondary};
        border-radius: 0 8px 8px 0;
        color: {text_secondary};
        font-style: italic;
    }}
    
    /* ── Tables ── */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 14px;
    }}
    th {{
        background-color: {bg_tertiary};
        color: {accent_teal};
        padding: 10px 14px;
        text-align: left;
        border-bottom: 2px solid {accent_blue};
        font-weight: 600;
    }}
    td {{
        padding: 10px 14px;
        border-bottom: 1px solid {border};
    }}
    tr:hover td {{
        background-color: {bg_hover};
    }}
    
    /* ── Math Display ── */
    .MathJax {{ 
        overflow-x: auto; 
        font-size: 110% !important;
    }}
    mjx-container[display="true"] {{
        margin: 20px 0 !important;
        padding: 12px;
        background: {bg_secondary};
        border-radius: 8px;
        border-left: 3px solid {accent_purple};
    }}
    
    /* ── Custom Callout Boxes ── */
    .callout {{
        margin: 20px 0;
        padding: 16px 20px;
        border-radius: 8px;
        border-left: 4px solid;
        font-size: 14px;
    }}
    .callout-title {{
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .callout-analogy {{
        background-color: rgba(227, 179, 65, 0.08);
        border-color: {accent_gold};
    }}
    .callout-analogy .callout-title {{ color: {accent_gold}; }}
    
    .callout-aha {{
        background-color: rgba(63, 185, 162, 0.08);
        border-color: {accent_teal};
    }}
    .callout-aha .callout-title {{ color: {accent_teal}; }}
    
    .callout-code {{
        background-color: rgba(88, 166, 255, 0.08);
        border-color: {accent_blue};
    }}
    .callout-code .callout-title {{ color: {accent_blue}; }}
    
    .callout-why {{
        background-color: rgba(188, 140, 255, 0.08);
        border-color: {accent_purple};
    }}
    .callout-why .callout-title {{ color: {accent_purple}; }}
    
    .callout-warning {{
        background-color: rgba(248, 81, 73, 0.08);
        border-color: {accent_red};
    }}
    .callout-warning .callout-title {{ color: {accent_red}; }}
    
    .callout-challenge {{
        background-color: rgba(63, 185, 80, 0.08);
        border-color: {accent_green};
    }}
    .callout-challenge .callout-title {{ color: {accent_green}; }}
    
    /* ── Horizontal Rule ── */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, {border}, transparent);
        margin: 32px 0;
    }}
    
    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: {bg_primary}; }}
    ::-webkit-scrollbar-thumb {{ background: {border}; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {text_secondary}; }}
</style>
</head>
<body>
{content}
</body>
</html>
""".format(**COLORS, content="{content}")
