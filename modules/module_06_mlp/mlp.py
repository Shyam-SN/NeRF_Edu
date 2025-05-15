import torch
import torch.nn as nn

class Tiny2DMLP(nn.Module):
    """
    A tiny MLP that takes a 2D coordinate (x, y) and predicts a scalar intensity [0, 1].
    Used to demonstrate how MLPs can memorize a 2D field.
    """
    def __init__(self, hidden_dim=64):
        super().__init__()
        
        # 4 hidden layers
        self.net = nn.Sequential(
            nn.Linear(2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid() # Squashes output to [0, 1]
        )

    def forward(self, x):
        return self.net(x)

def get_training_grid(size=32):
    """
    Generates a 2D grid of coordinates [-1, 1] and a target circular pattern.
    """
    x = torch.linspace(-1, 1, size)
    y = torch.linspace(-1, 1, size)
    Y, X = torch.meshgrid(y, x, indexing='ij')
    
    # Shape: (size*size, 2)
    coords = torch.stack([X.flatten(), Y.flatten()], dim=1)
    
    # Target pattern: A soft circle in the middle
    radius = torch.sqrt(coords[:, 0]**2 + coords[:, 1]**2)
    target = torch.exp(-5.0 * radius**2).unsqueeze(1) # Gaussian blob
    
    return coords, target
