import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .pipeline import render_pixel

class RenderThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(np.ndarray)
    
    def __init__(self, W, H):
        super().__init__()
        self.W = W
        self.H = H
        
    def run(self):
        focal = self.W  # Field of view approx 53 degrees
        near = 2.0
        far = 6.0
        n_samples = 64
        
        # Identity pose, looking down -Z
        c2w = np.eye(4)
        
        image = np.zeros((self.H, self.W, 3))
        
        total_pixels = self.W * self.H
        
        for v in range(self.H):
            for u in range(self.W):
                color = render_pixel(u, v, self.W, self.H, focal, c2w, near, far, n_samples)
                image[v, u] = color
                
            self.progress.emit(int((v / self.H) * 100))
            
        self.progress.emit(100)
        self.finished.emit(image)

class PipelineWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.W = 64
        self.H = 64
        self.image = np.zeros((self.H, self.W, 3))
        
        self.setup_ui()
        self.update_plot()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Plot Canvas
        self.figure = Figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        main_layout.addWidget(self.canvas)

        # Controls
        control_group = QGroupBox("Full Pipeline Render (64x64 resolution)")
        control_layout = QVBoxLayout(control_group)

        self.btn_render = QPushButton("Cast 4,096 Rays -> Render Image!")
        self.btn_render.clicked.connect(self.start_render)
        control_layout.addWidget(self.btn_render)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        control_layout.addWidget(self.progress_bar)

        main_layout.addWidget(control_group)

    def start_render(self):
        self.btn_render.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.thread = RenderThread(self.W, self.H)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.on_render_finished)
        self.thread.start()

    def on_render_finished(self, image):
        self.image = image
        self.btn_render.setEnabled(True)
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        
        self.ax.imshow(self.image)
        self.ax.set_title("NeRF Output Image")
        self.ax.axis('off')
        
        self.canvas.draw_idle()
