# 📐 Module 3: Linear Algebra for NeRF

Matrices are the silent workhorses of NeRF. Every time we rotate a camera, transform a ray, or push data through a neural network layer, we're multiplying matrices. This module builds the visual intuition for what matrix multiplication *actually does to space*.

---

## 1. What a Matrix *Really* Is

> [!ANALOGY] 🧘 The Yoga Mat Analogy: Imagine the 2D coordinate plane is a rubber yoga mat with a grid drawn on it. A matrix $A$ is a set of *yoga instructions*: "stretch left by 2×," "shear diagonally," "rotate 45°." When you apply $A$ to a vector, you're asking: *"If I deform the yoga mat according to these instructions, where does my vector end up?"*

A matrix is **not** just a table of numbers. It is a **linear transformation** — a recipe for warping space. The key rules:

1. The origin $(0, 0)$ stays fixed (the pin in the center of the yoga mat never moves).
2. Grid lines remain **straight and evenly spaced** after transformation (no curves or bubbles).

When you compute $A\mathbf{v}$, you're asking: *"Where does vector $\mathbf{v}$ land after the space-warp $A$?"*

---

## 2. Basis Vectors — The Columns Tell All

A $2 \times 2$ matrix is completely defined by where it sends the two standard basis vectors:

- $\hat{\mathbf{i}} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ (pointing right)
- $\hat{\mathbf{j}} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ (pointing up)

For matrix $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$:

- **Column 1** $= \begin{bmatrix} a \\ c \end{bmatrix}$ is where $\hat{\mathbf{i}}$ lands
- **Column 2** $= \begin{bmatrix} b \\ d \end{bmatrix}$ is where $\hat{\mathbf{j}}$ lands

> [!AHA] This is why the rotation matrix $R$ in Module 2 works: its columns ARE the camera's axes expressed in world coordinates. Column 1 = where the camera's "right" direction points in the world. It's literally the definition of a rotation — "where do my basis vectors end up?"

Every other vector in space is just a linear combination of $\hat{\mathbf{i}}$ and $\hat{\mathbf{j}}$, so it follows them to its new location automatically.

```python
import numpy as np

A = np.array([[2, -1],
              [1,  1]])

# Where does i-hat land?
i_hat_new = A @ np.array([1, 0])  # → [2, 1]

# Where does j-hat land?  
j_hat_new = A @ np.array([0, 1])  # → [-1, 1]

# Where does ANY vector land? (it's just a combo of i and j)
v = np.array([3, 2])
result = A @ v  # = 3 * [2,1] + 2 * [-1,1] = [4, 5]
```

---

## 3. The Determinant — Area Scaling

The **determinant** $\det(A)$ tells you how much the transformation scales area:

- $\det(A) = 1$ → area is preserved (pure rotation)
- $\det(A) = 2$ → area doubles  
- $\det(A) = 0$ → space is collapsed to a line (information is destroyed!)
- $\det(A) < 0$ → space is flipped (mirror image)

> [!WHY] 🤔 Wait, But Why? — In NeRF, rotation matrices always have $\det(R) = 1$ (they preserve volume and don't flip space). If your rotation matrix has a determinant that isn't 1, something is wrong with your camera calibration!

---

## 4. Eigenvectors and Eigenvalues

When you warp the yoga mat, most vectors get knocked off their original direction. But there are special vectors that **refuse to rotate** — they only get stretched or squished along their original line. These are **eigenvectors**.

$$
A\mathbf{v} = \lambda\mathbf{v}
$$

- $\mathbf{v}$ = **Eigenvector** (the stubborn direction that won't rotate)
- $\lambda$ = **Eigenvalue** (how much it gets stretched: $\lambda > 1$ = stretched, $0 < \lambda < 1$ = squished, $\lambda < 0$ = flipped)

> [!CODE] 💻 Computing eigenvectors in NumPy:

```python
A = np.array([[2, 1],
              [1, 2]])

eigenvalues, eigenvectors = np.linalg.eig(A)
# eigenvalues = [3, 1]
# eigenvectors = [[0.707, -0.707], [0.707, 0.707]]
# Direction [1,1] gets stretched 3× — Direction [1,-1] stays the same
```

> [!WHY] 🤔 Wait, But Why? — When training NeRF, the eigenvalues of the **Hessian matrix** (second derivatives of the loss) control the curvature of the loss landscape. If eigenvalues vary wildly (e.g., 0.001 and 1000), gradient descent oscillates chaotically — this is the *spectral bias* problem we'll solve in Module 7 with Positional Encoding!

---

## 5. Experiment

In the interactive visualizer, manipulate a $2 \times 2$ matrix by changing $(a, b, c, d)$:

1. Start with the **identity** ($a=1, b=0, c=0, d=1$). The grid is undistorted.
2. Set $a=2$ — watch $\hat{\mathbf{i}}$ stretch to twice its length (scaling).
3. Set $b=1$ — watch the grid **shear** (tilting $\hat{\mathbf{j}}$).
4. Try $a=0, b=-1, c=1, d=0$ — this is a **90° rotation**!
5. Look at the **blue eigenvector** — notice how it only scales, never rotates, even as the grid warps around it.

> [!CHALLENGE] 🏋️ Detective Work: Can you find a matrix where the eigenvectors point along the diagonal directions $(1,1)$ and $(1,-1)$? Hint: try a symmetric matrix like $\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$.
