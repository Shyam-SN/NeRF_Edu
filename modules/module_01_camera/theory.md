# 📷 Module 1: How Images Are Formed

Before we can teach a neural network to render 3D scenes, we need to understand the single most fundamental operation in all of computer vision: **how a 3D world gets squished onto a 2D image.**

---

## 1. The Pinhole Camera

> [!ANALOGY] 🍕 Pizza Box Camera: Poke a tiny hole in a pizza box. Hold it up to a sunny window. Light rays from outside squeeze through the tiny hole and project an upside-down image on the opposite wall. Congratulations — you just built a camera. The grease stain on the back wall? That's your image sensor. Leonardo da Vinci figured this out 500 years ago.

In a **pinhole camera**, only a single ray of light from each point in the scene can pass through the tiny aperture. Because light travels in straight lines, the projected image is **inverted** (flipped upside-down and left-right).

In computer graphics, we cheat: we place a **virtual image plane** *in front of* the camera center instead of behind it. This eliminates the inversion and makes the math cleaner.

---

## 2. Perspective Projection (The Core Math)

Let our camera center sit at the origin $(0, 0, 0)$.
We place the virtual image plane at distance $f$ (the **focal length**) along the Z-axis.

A 3D point $P = (X, Y, Z)$ projects onto the image plane at $Z = f$ by **similar triangles**:

$$
x = f \cdot \frac{X}{Z}, \quad y = f \cdot \frac{Y}{Z}
$$

> [!AHA] This is perspective projection in two lines of math. Objects further away ($Z$ is large) project closer to the center. Objects close up ($Z$ is small) project further out. This is why railroad tracks appear to converge — pure geometry.

---

## 3. The Intrinsic Matrix ($K$)

Real camera sensors measure in **pixels**, not meters. We need to convert physical coordinates $(x, y)$ to pixel indices $(u, v)$:

- $f_x, f_y$ — Focal length in **pixel units** (pixels per meter × focal length in meters)
- $c_x, c_y$ — The **principal point** (where the optical axis hits the sensor, usually the image center)

The **Intrinsic Matrix** $K$ encodes this conversion:

$$
K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}
$$

The full projection from a 3D camera-space point to a 2D pixel:

$$
\begin{bmatrix} u \cdot Z_c \\ v \cdot Z_c \\ Z_c \end{bmatrix} = K \begin{bmatrix} X_c \\ Y_c \\ Z_c \end{bmatrix}
$$

Divide by $Z_c$ to get your final pixel coordinates $(u, v)$.

> [!CODE] 💻 Show Me The Code — Here's the projection in 3 lines of Python:

```python
def project_point(fx, fy, cx, cy, X, Y, Z):
    u = (fx * X) / abs(Z) + cx   # X → pixel column
    v = (fy * Y) / abs(Z) + cy   # Y → pixel row
    return (u, v)
```

---

## 4. Ray Generation (The NeRF Twist)

> [!WHY] 🤔 Wait, But Why? — In traditional graphics, we project 3D → 2D (rendering). In NeRF, we do the **exact opposite**: we go from 2D → 3D. For every pixel $(u, v)$ on the screen, we shoot a ray *backward* into 3D space to figure out what color it should be. This is called **inverse projection**.

To find the ray direction $\mathbf{d}_{cam}$ in camera coordinates for pixel $(u, v)$:

$$
\mathbf{d}_{cam} = \begin{bmatrix} \frac{u - c_x}{f_x} \\ -\frac{v - c_y}{f_y} \\ -1 \end{bmatrix}
$$

*(We use the OpenGL convention: camera looks down $-Z$, $Y$ is up, hence the negatives.)*

```python
def generate_ray(u, v, fx, fy, cx, cy):
    dir_x = (u - cx) / fx
    dir_y = -(v - cy) / fy
    dir_z = -1.0
    
    direction = np.array([dir_x, dir_y, dir_z])
    direction = direction / np.linalg.norm(direction)  # normalize!
    return direction
```

---

## 5. Experiment

In the interactive visualizer on the right, try adjusting:

1. **Focal Length ($f$)**: Increasing $f$ narrows the Field of View — like zooming in with a telephoto lens. Decreasing $f$ widens it — like a fisheye.
2. **Point Depth ($Z$)**: Objects further away project closer to the center (perspective foreshortening).
3. **Point X**: Slide the 3D point left/right and watch the projected point move on the sensor.

> [!CHALLENGE] 🏋️ Mental Math: If $f_x = 500$ pixels, $c_x = 400$ pixels, and a bird is at 3D position $(3, 2, -10)$, what pixel column $u$ does it project to? Answer: $u = 500 \times 3 / 10 + 400 = 550$. Try verifying this with the sliders!
