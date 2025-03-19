import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .math_impl import apply_transformation, get_eigenvectors

class LinalgWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_plot()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Plot Canvas
        self.figure = Figure(figsize=(6, 5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        main_layout.addWidget(self.canvas)

        # Controls
        control_group = QGroupBox("2x2 Transformation Matrix A")
        control_layout = QGridLayout(control_group)

        # A = [[a, b], [c, d]]
        control_layout.addWidget(QLabel("a:"), 0, 0)
        self.slider_a = self.create_slider(-30, 30, 10, 0, 1, control_layout) # scaled by 10

        control_layout.addWidget(QLabel("b:"), 0, 2)
        self.slider_b = self.create_slider(-30, 30, 0, 0, 3, control_layout)

        control_layout.addWidget(QLabel("c:"), 1, 0)
        self.slider_c = self.create_slider(-30, 30, 0, 1, 1, control_layout)

        control_layout.addWidget(QLabel("d:"), 1, 2)
        self.slider_d = self.create_slider(-30, 30, 10, 1, 3, control_layout)

        main_layout.addWidget(control_group)
        
        # Grid generation
        x = np.linspace(-5, 5, 11)
        y = np.linspace(-5, 5, 11)
        X, Y = np.meshgrid(x, y)
        self.grid_points = np.vstack([X.flatten(), Y.flatten()])

    def create_slider(self, min_val, max_val, init_val, row, col, layout):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(init_val)
        slider.valueChanged.connect(self.update_plot)
        layout.addWidget(slider, row, col)
        return slider

    def update_plot(self):
        self.ax.clear()
        
        # Get Matrix A
        a = self.slider_a.value() / 10.0
        b = self.slider_b.value() / 10.0
        c = self.slider_c.value() / 10.0
        d = self.slider_d.value() / 10.0
        A = np.array([[a, b], [c, d]])
        
        # Transform Grid
        transformed_grid = apply_transformation(A, self.grid_points)
        
        # Plot transformed grid points
        self.ax.scatter(transformed_grid[0, :], transformed_grid[1, :], color='lightgray', s=10)
        
        # Plot basis vectors
        i_hat = np.array([1, 0])
        j_hat = np.array([0, 1])
        new_i = A @ i_hat
        new_j = A @ j_hat
        
        self.ax.quiver(0, 0, new_i[0], new_i[1], angles='xy', scale_units='xy', scale=1, color='r', label='Transformed i-hat')
        self.ax.quiver(0, 0, new_j[0], new_j[1], angles='xy', scale_units='xy', scale=1, color='g', label='Transformed j-hat')
        
        # Plot Eigenvectors
        eigenvectors, eigenvalues = get_eigenvectors(A)
        colors = ['b', 'm']
        for idx, (vec, val) in enumerate(zip(eigenvectors, eigenvalues)):
            # Scale eigenvector by its eigenvalue to show the stretching
            scaled_vec = vec * val
            self.ax.quiver(0, 0, scaled_vec[0], scaled_vec[1], angles='xy', scale_units='xy', scale=1, color=colors[idx], width=0.015, label=f'Eigenvector $\\lambda={val:.1f}$')
            # Also plot original eigenvector direction dashed
            self.ax.plot([-vec[0]*10, vec[0]*10], [-vec[1]*10, vec[1]*10], color=colors[idx], linestyle='--', alpha=0.3)

        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.ax.set_aspect('equal')
        self.ax.axhline(0, color='black',linewidth=1)
        self.ax.axvline(0, color='black',linewidth=1)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.legend(loc='upper right', fontsize='small')
        
        self.canvas.draw()
