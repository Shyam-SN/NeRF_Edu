import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .transform import create_c2w_matrix, transform_point

class CoordinatesWidget(QWidget):
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
        control_group = QGroupBox("Camera-to-World (c2w) Transformation")
        control_layout = QGridLayout(control_group)

        # Labels
        control_layout.addWidget(QLabel("Translation X:"), 0, 0)
        control_layout.addWidget(QLabel("Translation Y:"), 1, 0)
        control_layout.addWidget(QLabel("Translation Z:"), 2, 0)
        
        control_layout.addWidget(QLabel("Rotation X (Pitch):"), 0, 2)
        control_layout.addWidget(QLabel("Rotation Y (Yaw):"), 1, 2)
        control_layout.addWidget(QLabel("Rotation Z (Roll):"), 2, 2)

        # Sliders
        self.tx = self.create_slider(-5, 5, 2, 0, 1, control_layout)
        self.ty = self.create_slider(-5, 5, 2, 1, 1, control_layout)
        self.tz = self.create_slider(-5, 5, 2, 2, 1, control_layout)

        self.rx = self.create_slider(-180, 180, 0, 0, 3, control_layout)
        self.ry = self.create_slider(-180, 180, 45, 1, 3, control_layout)
        self.rz = self.create_slider(-180, 180, 0, 2, 3, control_layout)

        main_layout.addWidget(control_group)

    def create_slider(self, min_val, max_val, init_val, row, col, layout):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(init_val)
        slider.valueChanged.connect(self.update_plot)
        layout.addWidget(slider, row, col)
        return slider

    def update_plot(self):
        self.ax.clear()
        
        # World Origin (Fixed)
        self.ax.scatter(0, 0, 0, color='k', s=100, label='World Origin')
        # Draw World Axes
        world_len = 2.0
        self.ax.plot([0, world_len], [0, 0], [0, 0], color='r', linestyle='--', alpha=0.5)
        self.ax.plot([0, 0], [0, world_len], [0, 0], color='g', linestyle='--', alpha=0.5)
        self.ax.plot([0, 0], [0, 0], [0, world_len], color='b', linestyle='--', alpha=0.5)
        
        # Get Transform
        c2w = create_c2w_matrix(
            self.tx.value(), self.ty.value(), self.tz.value(),
            self.rx.value(), self.ry.value(), self.rz.value()
        )
        
        # Transform Camera Origin (0,0,0) to World
        cam_origin = transform_point(c2w, np.array([0,0,0]))
        self.ax.scatter(*cam_origin, color='m', s=100, label='Camera Origin (c2w * [0,0,0,1])')

        # Transform Camera Axes to World
        cam_x = transform_point(c2w, np.array([1,0,0]))
        cam_y = transform_point(c2w, np.array([0,1,0]))
        cam_z = transform_point(c2w, np.array([0,0,1]))

        self.ax.plot([cam_origin[0], cam_x[0]], [cam_origin[1], cam_x[1]], [cam_origin[2], cam_x[2]], color='r', linewidth=2, label='Camera X (Right)')
        self.ax.plot([cam_origin[0], cam_y[0]], [cam_origin[1], cam_y[1]], [cam_origin[2], cam_y[2]], color='g', linewidth=2, label='Camera Y (Up)')
        self.ax.plot([cam_origin[0], cam_z[0]], [cam_origin[1], cam_z[1]], [cam_origin[2], cam_z[2]], color='b', linewidth=2, label='Camera Z (Backward)')

        # Draw Frustum pointing down -Z (OpenGL convention)
        frustum_z = -1.0
        scale = 0.5
        corners = [
            np.array([scale, scale, frustum_z]),
            np.array([-scale, scale, frustum_z]),
            np.array([-scale, -scale, frustum_z]),
            np.array([scale, -scale, frustum_z])
        ]
        world_corners = [transform_point(c2w, c) for c in corners]
        
        for i in range(4):
            # Connect camera origin to frustum corners
            self.ax.plot([cam_origin[0], world_corners[i][0]], 
                         [cam_origin[1], world_corners[i][1]], 
                         [cam_origin[2], world_corners[i][2]], color='gray', alpha=0.5)
            # Connect frustum corners to each other
            self.ax.plot([world_corners[i][0], world_corners[(i+1)%4][0]], 
                         [world_corners[i][1], world_corners[(i+1)%4][1]], 
                         [world_corners[i][2], world_corners[(i+1)%4][2]], color='gray', alpha=0.5)

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)
        self.ax.set_xlabel('World X')
        self.ax.set_ylabel('World Y')
        self.ax.set_zlabel('World Z')
        self.ax.legend(loc='upper left', fontsize='small')
        
        self.canvas.draw()
