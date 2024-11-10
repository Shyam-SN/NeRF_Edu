import os
import re
import markdown
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .styles import THEORY_HTML_TEMPLATE

class TheoryViewer(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0d1117; border: none;")

    def _process_callouts(self, html):
        """
        Convert custom markdown callout syntax into styled HTML divs.
        
        Syntax in .md files (uses blockquote-like notation):
            > [!ANALOGY] Title text
            > Body content here
            
            > [!AHA] Title text
            > Body content  
            
            > [!CODE] Title text
            > Body content
            
            > [!WHY] Title text
            > Body content
            
            > [!WARNING] Title text
            > Body content
            
            > [!CHALLENGE] Title text
            > Body content
        """
        callout_icons = {
            "ANALOGY":   "🍕",
            "AHA":       "💡",
            "CODE":      "💻",
            "WHY":       "🤔",
            "WARNING":   "⚠️",
            "CHALLENGE": "🏋️",
        }
        
        callout_css_class = {
            "ANALOGY":   "callout-analogy",
            "AHA":       "callout-aha",
            "CODE":      "callout-code",
            "WHY":       "callout-why",
            "WARNING":   "callout-warning",
            "CHALLENGE": "callout-challenge",
        }
        
        # Pattern: match blockquotes that start with [!TYPE]
        # The markdown library converts > lines to <blockquote><p>...</p></blockquote>
        pattern = r'<blockquote>\s*<p>\[!(ANALOGY|AHA|CODE|WHY|WARNING|CHALLENGE)\]\s*(.*?)</p>\s*</blockquote>'
        
        def replace_callout(match):
            ctype = match.group(1)
            content = match.group(2)
            icon = callout_icons.get(ctype, "📌")
            css_class = callout_css_class.get(ctype, "callout-aha")
            
            # Split the first line (title) from the rest (body)
            lines = content.split('<br', 1)
            if len(lines) > 1:
                title = lines[0].strip()
                body = '<br' + lines[1]
            else:
                # Try splitting on first period or colon for a natural title
                title = content
                body = ""
            
            return f'''<div class="callout {css_class}">
                <div class="callout-title">{icon} {title}</div>
                {f'<div>{body}</div>' if body else ''}
            </div>'''
        
        html = re.sub(pattern, replace_callout, html, flags=re.DOTALL)
        return html

    def load_markdown(self, filepath):
        if not os.path.exists(filepath):
            self.setHtml(f"<h3>Error</h3><p>File not found: {filepath}</p>")
            return
            
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            
        # Convert Markdown to HTML
        html = markdown.markdown(
            text, 
            extensions=['fenced_code', 'tables', 'nl2br', 'sane_lists']
        )
        
        # Process custom callout boxes
        html = self._process_callouts(html)
        
        # Inject into the dark-themed template
        styled_html = THEORY_HTML_TEMPLATE.replace("{content}", html)
        self.setHtml(styled_html)
