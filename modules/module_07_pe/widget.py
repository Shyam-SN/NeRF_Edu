import torch
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox, QCheckBox, QSlider
)
from PyQt6.QtCore import Qt, QTimer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .pe import FunctionFitterMLP, get_1d_target_function

class PEWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.x, self.y = get_1d_target_function(300)
        
        self.step_count = 0
        self.is_training = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.train_step)
        
        self.setup_ui()
        self.reset_model()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Plot Canvas
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.figure.tight_layout(pad=2.0)
        main_layout.addWidget(self.canvas)

        # Controls
        control_group = QGroupBox("Positional Encoding Experiment")
        control_layout = QVBoxLayout(control_group)
        
        row1 = QHBoxLayout()
        self.chk_pe = QCheckBox("Use Positional Encoding (L=4)")
        self.chk_pe.stateChanged.connect(self.reset_model)
        row1.addWidget(self.chk_pe)
        
        self.lbl_status = QLabel("Step: 0 | Loss: N/A")
        row1.addWidget(self.lbl_status)
        control_layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.btn_train = QPushButton("Start Training")
        self.btn_train.clicked.connect(self.toggle_training)
        row2.addWidget(self.btn_train)

        self.btn_reset = QPushButton("Reset MLP")
        self.btn_reset.clicked.connect(self.reset_model)
        row2.addWidget(self.btn_reset)
        control_layout.addLayout(row2)

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
        use_pe = self.chk_pe.isChecked()
        self.model = FunctionFitterMLP(use_pe=use_pe, L=4)
        # Give higher LR to standard MLP to prove it's not a learning rate issue
        lr = 0.005 if use_pe else 0.01 
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.loss_fn = torch.nn.MSELoss()
        
        self.step_count = 0
        self.lbl_status.setText("Step: 0 | Loss: N/A")
        self.update_plot()

    def train_step(self):
        pred = self.model(self.x)
        loss = self.loss_fn(pred, self.y)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.step_count += 1
        
        if self.step_count % 5 == 0:
            self.lbl_status.setText(f"Step: {self.step_count} | Loss: {loss.item():.4f}")
            self.update_plot(pred.detach())

    def update_plot(self, pred=None):
        self.ax.clear()
        
        # Target Function
        self.ax.plot(self.x.numpy(), self.y.numpy(), 'k-', linewidth=3, label="Target High-Freq Signal", alpha=0.5)
        
        # Pred Function
        if pred is None:
            with torch.no_grad():
                pred = self.model(self.x)
                
        self.ax.plot(self.x.numpy(), pred.numpy(), 'r--', linewidth=2, label="MLP Prediction")
        
        self.ax.set_ylim(-2, 2)
        self.ax.set_title("Spectral Bias Demonstration")
        self.ax.legend(loc="upper right")
        
        self.canvas.draw_idle()
