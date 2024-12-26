import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QGroupBox
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .simulator import CameraSimulator

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_plot()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Plot Canvas
        self.figure = Figure(figsize=(6, 5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')
        
        main_layout.addWidget(self.canvas)

        # Controls
        control_group = QGroupBox("Camera Parameters")
        control_layout = QVBoxLayout(control_group)

        # Focal Length Slider
        row_f = QHBoxLayout()
        row_f.addWidget(QLabel("Focal Length (f):"))
        self.slider_f = QSlider(Qt.Orientation.Horizontal)
        self.slider_f.setRange(50, 400)
        self.slider_f.setValue(200)
        self.slider_f.valueChanged.connect(self.update_plot)
        row_f.addWidget(self.slider_f)
        control_layout.addLayout(row_f)

        # Point Z Slider
        row_z = QHBoxLayout()
        row_z.addWidget(QLabel("Point Depth (Z):"))
        self.slider_z = QSlider(Qt.Orientation.Horizontal)
        self.slider_z.setRange(-10, -2) # Negative Z
        self.slider_z.setValue(-5)
        self.slider_z.valueChanged.connect(self.update_plot)
        row_z.addWidget(self.slider_z)
        control_layout.addLayout(row_z)

        # Point X Slider
        row_x = QHBoxLayout()
        row_x.addWidget(QLabel("Point X:"))
        self.slider_x = QSlider(Qt.Orientation.Horizontal)
        self.slider_x.setRange(-5, 5)
        self.slider_x.setValue(2)
        self.slider_x.valueChanged.connect(self.update_plot)
        row_x.addWidget(self.slider_x)
        control_layout.addLayout(row_x)

        main_layout.addWidget(control_group)

    def update_plot(self):
        self.ax.clear()
        
        focal_length = self.slider_f.value()
        pt_z = self.slider_z.value()
        pt_x = self.slider_x.value()
        pt_y = 2 # fixed Y for simplicity
        
        # Draw Camera Center
        self.ax.scatter(0, 0, 0, color='r', s=100, label='Camera Center (0,0,0)')
        
        # Draw Image Plane (Virtual, so placed at Z = -1 * scale for visualization)
        # We will visualize it scaled down for ease of viewing
        sensor_z = -1.0
        # Sensor bounds
        sx = [-1, 1, 1, -1, -1]
        sy = [-1, -1, 1, 1, -1]
        sz = [sensor_z] * 5
        self.ax.plot(sx, sy, sz, color='k', alpha=0.3, label='Virtual Sensor Plane')
        
        # Draw 3D Point
        self.ax.scatter(pt_x, pt_y, pt_z, color='b', s=50, label='3D Point (X,Y,Z)')
        
        # Draw Ray from Camera to Point
        self.ax.plot([0, pt_x], [0, pt_y], [0, pt_z], color='orange', linestyle='--', label='Light Ray')
        
        # Calculate Intersection with Virtual Sensor (Z=-1)
        inter_x = pt_x / abs(pt_z)
        inter_y = pt_y / abs(pt_z)
        self.ax.scatter(inter_x, inter_y, sensor_z, color='g', s=50, label='Projected 2D Point')

        # FOV visualization (lines from center through corners of sensor)
        for vx, vy in zip([1,-1,-1,1], [1,1,-1,-1]):
            # The FOV is dictated by sensor size vs focal length.
            # A larger focal length means narrower FOV. We simulate this by scaling the frustum rays
            scale = 200.0 / focal_length
            self.ax.plot([0, vx*scale*abs(pt_z)], [0, vy*scale*abs(pt_z)], [0, pt_z], color='gray', alpha=0.2)

        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_zlim(-10, 1)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.legend(loc='upper left', fontsize='small')
        
        self.canvas.draw()
