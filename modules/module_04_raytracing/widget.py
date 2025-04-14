import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QGroupBox, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .ray_marcher import generate_ray_samples

class RayMarchingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Timer for animating stratified jitter
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(500) # 2 FPS update
        
        self.update_plot()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Plot Canvas
        self.figure = Figure(figsize=(6, 5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')
        
        main_layout.addWidget(self.canvas)

        # Controls
        control_group = QGroupBox("Ray Marching Parameters")
        control_layout = QVBoxLayout(control_group)

        # N_samples
        row_n = QHBoxLayout()
        row_n.addWidget(QLabel("Number of Samples (N):"))
        self.slider_n = QSlider(Qt.Orientation.Horizontal)
        self.slider_n.setRange(4, 64)
        self.slider_n.setValue(16)
        self.slider_n.valueChanged.connect(self.update_plot)
        row_n.addWidget(self.slider_n)
        control_layout.addLayout(row_n)

        # Near Plane
        row_near = QHBoxLayout()
        row_near.addWidget(QLabel("Near Plane (t_near):"))
        self.slider_near = QSlider(Qt.Orientation.Horizontal)
        self.slider_near.setRange(1, 40) # scaled by 10 (0.1 to 4.0)
        self.slider_near.setValue(10)
        self.slider_near.valueChanged.connect(self.update_plot)
        row_near.addWidget(self.slider_near)
        control_layout.addLayout(row_near)
        
        # Far Plane
        row_far = QHBoxLayout()
        row_far.addWidget(QLabel("Far Plane (t_far):"))
        self.slider_far = QSlider(Qt.Orientation.Horizontal)
        self.slider_far.setRange(41, 100) # scaled by 10 (4.1 to 10.0)
        self.slider_far.setValue(80)
        self.slider_far.valueChanged.connect(self.update_plot)
        row_far.addWidget(self.slider_far)
        control_layout.addLayout(row_far)

        # Stratified Checkbox
        self.chk_stratified = QCheckBox("Enable Stratified Sampling (Jitter)")
        self.chk_stratified.setChecked(True)
        self.chk_stratified.stateChanged.connect(self.update_plot)
        control_layout.addWidget(self.chk_stratified)

        main_layout.addWidget(control_group)

    def update_plot(self):
        self.ax.clear()
        
        n_samples = self.slider_n.value()
        near = self.slider_near.value() / 10.0
        far = self.slider_far.value() / 10.0
        stratified = self.chk_stratified.isChecked()
        
        origin = np.array([0.0, 0.0, 0.0])
        # A simple ray pointing forward and slightly up/right
        direction = np.array([0.2, 0.2, 1.0])
        direction = direction / np.linalg.norm(direction)
        
        pts, z_vals = generate_ray_samples(origin, direction, near, far, n_samples, stratified)
        
        # Draw Camera Origin
        self.ax.scatter(*origin, color='k', s=100, label='Camera Origin (o)')
        
        # Draw full ray line (from origin to far)
        end_pt = origin + direction * (far + 2.0)
        self.ax.plot([origin[0], end_pt[0]], 
                     [origin[1], end_pt[1]], 
                     [origin[2], end_pt[2]], color='gray', linestyle='--', alpha=0.5, label='Ray Path')
        
        # Draw Sample Points
        self.ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color='orange', s=40, depthshade=True, label='Network Query Samples r(t)')
        
        # Visualize Bins (Near and Far bounds)
        near_pt = origin + direction * near
        far_pt = origin + direction * far
        self.ax.scatter(*near_pt, color='g', marker='|', s=200, label='Near Plane')
        self.ax.scatter(*far_pt, color='r', marker='|', s=200, label='Far Plane')

        self.ax.set_xlim(-1, 5)
        self.ax.set_ylim(-1, 5)
        self.ax.set_zlim(-1, 10)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.legend(loc='upper left', fontsize='small')
        
        # Optimize rendering slightly
        self.ax.set_box_aspect((1, 1, 2))
        self.canvas.draw_idle()
