# 🌊 Module 7: Positional Encoding

In Module 6, we saw that a standard MLP can learn smooth, blurry shapes. But what about the sharp edge of a leaf? The intricate texture of a brick wall? The fine wrinkles on a face? Standard MLPs fail catastrophically at these — and Positional Encoding is the fix.

---

## 1. The Problem: Spectral Bias

> [!ANALOGY] 🎸 The One-String Guitar Problem: Imagine trying to play Beethoven's 5th Symphony on a guitar with only ONE string tuned to a low bass note. You can play the broad, slow melody, but you absolutely cannot hit the high-pitched violin notes — you physically don't have a string that vibrates that fast. That's exactly the problem with feeding raw $(x, y, z)$ coordinates into an MLP. The network only has "low-frequency strings" and cannot represent sharp, high-frequency details.

Deep neural networks suffer from **Spectral Bias**: when trained on low-dimensional inputs like $(x, y, z)$, they naturally prioritize learning low-frequency (smooth, broad) features and severely struggle with high-frequency (sharp, detailed) variations.

Without fixing this, NeRF renders look like they've been smeared with vaseline — blurry, smooth, and devoid of detail.

> [!WHY] 🤔 Wait, But Why does this happen? — Mathematically, each ReLU layer in the MLP can only introduce ONE "bend" in the function per neuron. To represent a sharp edge, you need many bends close together. To represent fine texture, you need *thousands* of bends. With raw $(x,y,z)$ inputs, the gradients for high-frequency patterns are vanishingly small (the loss surface is nearly flat in those directions), so the optimizer gives up.

---

## 2. The Solution: Fourier Features

To give the network "high-frequency strings," we project our coordinates into a higher-dimensional space using sine and cosine functions at exponentially increasing frequencies.

For a single coordinate $p \in [-1, 1]$, the Positional Encoding $\gamma(p)$ with $L$ frequency bands:

$$
\gamma(p) = \left(\sin(2^0 \pi p),\; \cos(2^0 \pi p),\; \sin(2^1 \pi p),\; \cos(2^1 \pi p),\; \ldots,\; \sin(2^{L-1} \pi p),\; \cos(2^{L-1} \pi p)\right)
$$

This maps a 1D scalar to a $2L$-dimensional vector. For a 3D input $(x,y,z)$, we encode each coordinate separately and concatenate:

- Input: 3D coordinate
- Output: $3 \times (2L + 1) = 63$-dimensional vector (with $L = 10$, including the original coordinate)

```python
import torch

class PositionalEncoding(torch.nn.Module):
    def __init__(self, L=10):
        super().__init__()
        # Frequencies: π, 2π, 4π, 8π, ..., 2^(L-1)·π
        self.freqs = 2.0 ** torch.arange(L) * torch.pi
    
    def forward(self, x):
        """x: (N, D) → output: (N, D + D*2*L)"""
        encoded = [x]  # include original coordinate
        for freq in self.freqs:
            encoded.append(torch.sin(x * freq))
            encoded.append(torch.cos(x * freq))
        return torch.cat(encoded, dim=-1)
```

> [!AHA] Look at what happens to $x = 0.5$ with $L = 4$: instead of the network seeing just the number "0.5", it sees $[\sin(\pi \cdot 0.5), \cos(\pi \cdot 0.5), \sin(2\pi \cdot 0.5), \cos(2\pi \cdot 0.5), \ldots] = [1.0, 0.0, 0.0, -1.0, \ldots]$. The network can now distinguish between $x = 0.5$ and $x = 0.500001$ because the high-frequency sines oscillate rapidly between them!

---

## 3. Visual Intuition: Unrolling onto a Circle

Here's a beautiful geometric way to think about it:

When you compute $[\sin(\theta), \cos(\theta)]$ for an angle $\theta$, you're mapping a 1D number line onto a **circle** in 2D. Points that are close on the number line are close on the circle, but the circle also wraps around — giving the network a much richer representation to work with.

With $L$ frequencies, you're mapping onto $L$ circles of different sizes simultaneously — a **hypertorus** in $2L$-dimensional space. This is why the network can now distinguish arbitrarily fine details: nearby points that look identical in 1D become clearly separated on the high-frequency circles.

> [!CODE] 💻 The connection to Transformers: This is the same Positional Encoding used in Attention Is All You Need (2017). In Transformers, it encodes *token position*. In NeRF, it encodes *spatial position*. Same math, completely different domain!

---

## 4. How Many Frequencies?

The original NeRF paper uses:
- $L = 10$ for position $(x, y, z)$ → maps 3D to 63D
- $L = 4$ for viewing direction $(\theta, \phi)$ → maps 2D to 18D

> [!WHY] 🤔 Wait, But Why fewer frequencies for direction? — Viewing direction affects color smoothly (specular highlights are broad, not pixel-sharp). Position needs high frequencies for sharp geometry edges. Using too many frequencies for direction would cause flickering artifacts.

---

## 5. Experiment

In the interactive visualizer, we train an MLP to fit a bumpy 1D function ($\sin(4\pi x) + 0.5\cos(8\pi x)$):

1. **Without Positional Encoding**: Click Start Training. The MLP quickly learns the rough average but completely fails to capture the bumps. It converges to a nearly flat line. This is spectral bias.

2. **With Positional Encoding** ($L = 4$): Check the "Use Positional Encoding" box, click Reset, then Start Training. The network instantly snaps to the bumpy function within ~50 steps. The pre-computed sine/cosine features make the high-frequency bumps trivially easy to learn.

> [!CHALLENGE] 🏋️ Dimension Explosion: If we encode a 3D coordinate with $L = 10$, what is the output dimension? Answer: $3 \times (1 + 2 \times 10) = 63$. For $L = 20$, it would be $3 \times 41 = 123$. More frequencies = sharper details, but also more computation per MLP query.
