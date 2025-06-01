import torch
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .mlp import Tiny2DMLP, get_training_grid

class MLPWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.size = 32
        self.coords, self.target = get_training_grid(self.size)
        
        self.model = Tiny2DMLP(hidden_dim=32)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        self.loss_fn = torch.nn.MSELoss()
        
        self.step_count = 0
        self.is_training = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.train_step)
        
        self.setup_ui()
        self.update_plot()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Plot Canvas
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        
        self.ax_target = self.figure.add_subplot(121)
        self.ax_pred = self.figure.add_subplot(122)
        self.figure.tight_layout(pad=2.0)
        
        main_layout.addWidget(self.canvas)

        # Controls
        control_group = QGroupBox("MLP Training Controls")
        control_layout = QHBoxLayout(control_group)

        self.btn_train = QPushButton("Start Training")
        self.btn_train.clicked.connect(self.toggle_training)
        control_layout.addWidget(self.btn_train)

        self.btn_reset = QPushButton("Reset MLP")
        self.btn_reset.clicked.connect(self.reset_model)
        control_layout.addWidget(self.btn_reset)

        self.lbl_status = QLabel("Step: 0 | Loss: N/A")
        control_layout.addWidget(self.lbl_status)

        main_layout.addWidget(control_group)

    def toggle_training(self):
        if self.is_training:
            self.timer.stop()
            self.btn_train.setText("Start Training")
            self.is_training = False
        else:
            self.timer.start(50) # 20 FPS training
            self.btn_train.setText("Stop Training")
            self.is_training = True

    def reset_model(self):
        self.model = Tiny2DMLP(hidden_dim=32)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        self.step_count = 0
        self.lbl_status.setText("Step: 0 | Loss: N/A")
        self.update_plot()

    def train_step(self):
        # 1. Forward pass
        pred = self.model(self.coords)
        
        # 2. Compute Loss
        loss = self.loss_fn(pred, self.target)
        
        # 3. Backward pass and Optimize
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.step_count += 1
        
        # Update UI every 5 steps
        if self.step_count % 5 == 0:
            self.lbl_status.setText(f"Step: {self.step_count} | Loss: {loss.item():.4f}")
            self.update_plot(pred.detach())

    def update_plot(self, pred=None):
        self.ax_target.clear()
        self.ax_pred.clear()
        
        # Target image
        target_img = self.target.numpy().reshape(self.size, self.size)
        self.ax_target.imshow(target_img, cmap='viridis', origin='lower')
        self.ax_target.set_title("Target 2D Pattern")
        self.ax_target.axis('off')
        
        # Pred image
        if pred is None:
            with torch.no_grad():
                pred = self.model(self.coords)
                
        pred_img = pred.numpy().reshape(self.size, self.size)
        self.ax_pred.imshow(pred_img, cmap='viridis', origin='lower', vmin=0, vmax=1)
        self.ax_pred.set_title("MLP Prediction")
        self.ax_pred.axis('off')
        
        self.canvas.draw_idle()
