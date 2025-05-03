import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .volrend import compute_volume_rendering_weights

class VolumeRenderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_plot()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Plot Canvas
        self.figure = Figure(figsize=(6, 5))
        self.canvas = FigureCanvas(self.figure)
        # We will use 3 subplots: one for Density, one for Transmittance, one for Weights
        self.ax_sigma = self.figure.add_subplot(311)
        self.ax_trans = self.figure.add_subplot(312)
        self.ax_weight = self.figure.add_subplot(313)
        
        self.figure.tight_layout(pad=3.0)
        main_layout.addWidget(self.canvas)

        # Controls
        control_group = QGroupBox("Density at Sample Points")
        control_layout = QGridLayout(control_group)

        # 4 samples
        self.sliders = []
        for i in range(4):
            control_layout.addWidget(QLabel(f"Sample {i+1} Density (\u03c3):"), i, 0)
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100) # 0 to 10.0
            slider.setValue(10 if i == 1 else 0) # Sample 2 has some initial density
            slider.valueChanged.connect(self.update_plot)
            control_layout.addWidget(slider, i, 1)
            self.sliders.append(slider)

        main_layout.addWidget(control_group)

    def update_plot(self):
        self.ax_sigma.clear()
        self.ax_trans.clear()
        self.ax_weight.clear()
        
        # Get densities from sliders
        sigmas = np.array([s.value() / 10.0 for s in self.sliders])
        # Fixed distance between samples for simplicity
        dists = np.array([1.0, 1.0, 1.0, 1.0])
        
        alphas, transmittances, weights = compute_volume_rendering_weights(sigmas, dists)
        
        x = np.arange(1, 5)
        
        # Plot Density
        self.ax_sigma.bar(x, sigmas, color='gray')
        self.ax_sigma.set_ylabel('Density (\u03c3)')
        self.ax_sigma.set_ylim(0, 10)
        self.ax_sigma.set_xticks(x)
        self.ax_sigma.set_xticklabels([f'S{i}' for i in x])
        self.ax_sigma.set_title("1. Physical Volume Density")
        
        # Plot Transmittance
        self.ax_trans.plot(x, transmittances, marker='o', color='blue', linestyle='-', linewidth=2)
        self.ax_trans.set_ylabel('Transmittance ($T$)')
        self.ax_trans.set_ylim(0, 1.1)
        self.ax_trans.set_xticks(x)
        self.ax_trans.set_xticklabels([f'S{i}' for i in x])
        self.ax_trans.set_title("2. Light Surviving to Sample (Beer-Lambert)")

        # Plot Weights
        self.ax_weight.bar(x, weights, color='orange')
        self.ax_weight.set_ylabel('Weight (w = T \u00b7 \u03b1)')
        self.ax_weight.set_ylim(0, 1.1)
        self.ax_weight.set_xticks(x)
        self.ax_weight.set_xticklabels([f'S{i}' for i in x])
        self.ax_weight.set_title("3. Final Rendering Weight (Contribution to Pixel)")
        
        self.canvas.draw()
