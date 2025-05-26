# 🧠 Module 6: Multi-Layer Perceptrons (MLPs)

We now know how to march along a ray and compute the volume rendering integral — *if* we have density $\sigma$ and color $\mathbf{c}$ at every point in space. But where do those numbers come from?

---

## 1. The Neural Network as a 3D Scene

> [!ANALOGY] 🧠 The Lazy Oracle: Imagine a magical all-knowing oracle sitting in the center of a 3D scene. You can ask it: "Hey oracle, what's at position $(2.7, -1.3, 4.1)$ looking from direction $(0.5, 0.2, -0.8)$?" and it instantly replies: "Density 47.3, color (0.8, 0.2, 0.1)." You ask it this question **81 million times per image**. Instead of storing a billion Minecraft blocks in memory, the oracle memorizes the entire scene in its brain (network weights). It's like compressing a 3D world into a zip file... that you can query from any angle.

In traditional graphics, the 3D world is stored as a discrete **voxel grid** (3D array of colors). But $1024^3$ voxels = **1 billion parameters**, and it looks blocky up close.

NeRF instead uses a neural network as a **continuous mathematical function**:

$$
F_\Theta: (x, y, z, \theta, \phi) \rightarrow (\sigma, r, g, b)
$$

Feed it a 3D coordinate and a viewing direction → it outputs density and color. Because it's a continuous function, you can zoom in infinitely without seeing "pixels."

> [!AHA] The entire 3D scene is compressed into the network weights $\Theta$. A typical NeRF has ~1.2 million parameters — that's ~5 MB to store an entire photorealistic 3D scene. Compare that to a billion-voxel grid at 4 GB!

---

## 2. The NeRF Architecture

The NeRF MLP isn't a generic classifier. It's carefully designed to respect the **physics of light**:

### Stage 1: Geometry (Density)

Density represents *physical matter* — a rock doesn't disappear when you walk around it. Therefore, density is **view-independent**.

The first part of the MLP takes *only* the 3D position $(x, y, z)$ and processes it through **8 fully-connected layers** (each 256 neurons wide):

- Input: $(x, y, z)$ → after Positional Encoding (Module 7): 63-dim vector
- Output 1: Density $\sigma$ (activated with ReLU to ensure $\sigma \geq 0$)
- Output 2: A 256-dim **feature vector** (a latent description of the geometry)

### Stage 2: Appearance (Color)

Color *is* view-dependent! A shiny apple looks bright white when light bounces perfectly into your eye (specular highlight), but red from other angles.

The second part of the MLP:
- Input: 256-dim feature vector + viewing direction $\mathbf{d}$
- Architecture: 1 additional fully-connected layer
- Output: $(R, G, B)$ color (activated with Sigmoid to clamp to $[0, 1]$)

> [!WHY] 🤔 Wait, But Why split it? — If the color depended on position alone, NeRF couldn't model shiny surfaces (specular reflections change with viewpoint). But if density *also* depended on direction, the 3D geometry would change depending on where you look — which is physically impossible. The split enforces physical correctness.

---

## 3. Inside a Single Layer

Each layer of the MLP is just a **linear transformation** (Module 3!) followed by a non-linearity:

$$
\mathbf{h}_{i+1} = \text{ReLU}(W_i \mathbf{h}_i + \mathbf{b}_i)
$$

```python
import torch.nn as nn

# One MLP layer = Linear + ReLU
layer = nn.Sequential(
    nn.Linear(256, 256),  # Matrix multiply: W @ h + b
    nn.ReLU()             # Non-linearity: max(0, x)
)
```

> [!WARNING] ⚠️ Without ReLU, the entire 8-layer network collapses into a single matrix multiplication (because stacking linear operations is still linear). It would only be able to represent flat planes in 3D space — no curved surfaces, no complex geometry. ReLU is what gives the network its power to approximate *any* continuous function.

### The Skip Connection

NeRF adds a **skip connection** at layer 4: the original input is concatenated with the intermediate features. This helps gradient flow during training and lets the network "remember" the raw coordinates even deep in the network.

---

## 4. A Tiny MLP Demo

In this module's interactive widget, we train a **2D version** of NeRF's MLP:

- Input: 2D pixel coordinate $(x, y)$ normalized to $[-1, 1]$
- Output: Grayscale intensity $[0, 1]$
- Target: A circular Gaussian blob pattern

This is a "2D NeRF" — the network memorizes a 2D image as a continuous function. The same principle scales to 3D.

```python
class Tiny2DMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 32), nn.ReLU(),   # (x,y) → 32 features
            nn.Linear(32, 32), nn.ReLU(),  # hidden layer
            nn.Linear(32, 32), nn.ReLU(),  # hidden layer
            nn.Linear(32, 32), nn.ReLU(),  # hidden layer
            nn.Linear(32, 1), nn.Sigmoid() # → intensity [0,1]
        )
    
    def forward(self, xy):
        return self.net(xy)
```

> [!AHA] Training this tiny MLP is conceptually identical to training a real NeRF. The loss function is just MSE between the predicted and actual pixel values. The optimizer (Adam) adjusts weights to minimize this loss. Scale this to 3D with density and volume rendering, and you have NeRF.

---

## 5. Experiment

In the interactive visualizer:

1. Click **Start Training** — watch the MLP prediction (right) slowly converge toward the target pattern (left).
2. Notice the progression: the network first learns the broad, smooth shape (low frequencies), then fills in finer details (higher frequencies). This is **spectral bias** in action — Module 7 fixes it!
3. Click **Reset MLP** to reinitialize and watch a different random starting point converge to the same solution.

> [!CHALLENGE] 🏋️ Parameter Count: If the network has layers of sizes $[2, 32, 32, 32, 32, 1]$, how many total trainable parameters does it have? Count: $(2×32+32) + (32×32+32) × 3 + (32×1+1) = 96 + 3×1056 + 33 = 3297$ parameters. Now imagine NeRF with $[63, 256, 256, 256, 256, 256, 256, 256, 256, 1]$ — over 1.2 million!
