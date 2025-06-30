import torch
import torch.nn as nn
import numpy as np

class PositionalEncoding(nn.Module):
    def __init__(self, L=4):
        """
        L: number of frequency bands
        Output dimension will be 2 * L * input_dim + input_dim (if we include the original coordinate)
        """
        super().__init__()
        self.L = L
        # Create frequencies 2^0, 2^1, ..., 2^(L-1)
        self.freqs = 2.0 ** torch.linspace(0, L - 1, L) * torch.pi
        
    def forward(self, x):
        """
        x: (N, 1) tensor of coordinates
        Returns: (N, 1 + 2*L) encoded features
        """
        if self.L == 0:
            return x
            
        features = [x]
        for freq in self.freqs:
            features.append(torch.sin(x * freq))
            features.append(torch.cos(x * freq))
            
        return torch.cat(features, dim=-1)

class FunctionFitterMLP(nn.Module):
    def __init__(self, use_pe=False, L=4):
        super().__init__()
        
        self.pe = PositionalEncoding(L) if use_pe else PositionalEncoding(0)
        
        in_dim = 1 + 2 * L if use_pe else 1
        hidden_dim = 64
        
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1) # Output a scalar y
        )

    def forward(self, x):
        x_encoded = self.pe(x)
        return self.net(x_encoded)

def get_1d_target_function(n_points=200):
    """
    Generates a high-frequency 1D function to fit.
    y = sin(4 * pi * x) + 0.5 * cos(8 * pi * x)
    """
    x = torch.linspace(-1, 1, n_points).unsqueeze(1)
    # A bumpy function
    y = torch.sin(4 * torch.pi * x) + 0.5 * torch.cos(8 * torch.pi * x)
    return x, y
