# 🌍 Module 2: Coordinate Systems and Transformations

In Module 1 we learned to shoot rays from a camera. But we assumed the camera was sitting at the origin, perfectly aligned with the axes. What happens when we move the camera to photograph a scene from different angles? That's what this module is about.

---

## 1. World Space vs. Camera Space

> [!ANALOGY] 🕺 The GPS vs. Selfie Problem: Your phone's GPS uses **World Space** — latitude and longitude don't change when you turn your head. But your front-facing camera uses **Camera Space** — your nose is always at the center of the selfie, regardless of which direction you're facing. If you spin 180°, everything in your selfie changes, but GPS doesn't care. The statue in the park hasn't moved. Only your *perspective* changed.

Two coordinate systems, same universe:

- **World Space**: A fixed, global coordinate system. A statue at $(3, 0, 2)$ stays at $(3, 0, 2)$ no matter where you stand.
- **Camera Space**: A coordinate system attached to the camera. The camera's own position is always $(0, 0, 0)$, and it always looks down its local $-Z$ axis.

When the camera moves, the coordinates of objects *relative to the camera* change — even though nothing in the world has actually moved.

---

## 2. The Extrinsics Matrix ($c2w$)

To convert between these spaces, we use a $4 \times 4$ transformation matrix. In NeRF, the standard is the **Camera-to-World** ($c2w$) matrix:

$$
T_{c2w} = \begin{bmatrix} R & \mathbf{t} \\ \mathbf{0}^T & 1 \end{bmatrix}
$$

Where:
- $R$ is a $3 \times 3$ **Rotation Matrix** — it encodes the camera's orientation (which way it's pointing, its tilt, its roll). Its columns are the camera's local X, Y, Z axes expressed in world coordinates.
- $\mathbf{t}$ is a $3 \times 1$ **Translation Vector** — the camera's position in the world.

> [!AHA] The columns of $R$ literally tell you where the camera's axes point in the world. Column 1 = camera's "right" direction. Column 2 = camera's "up" direction. Column 3 = camera's "backward" direction. If you stack them as columns, you get $R$. That's all a rotation matrix is.

### Transforming a Point

To find where a camera-space point $P_{cam}$ is located in the world:

$$
P_{world} = R \cdot P_{cam} + \mathbf{t}
$$

Or equivalently, using homogeneous coordinates:

$$
\begin{bmatrix} X_{world} \\ Y_{world} \\ Z_{world} \\ 1 \end{bmatrix} = T_{c2w} \begin{bmatrix} X_{cam} \\ Y_{cam} \\ Z_{cam} \\ 1 \end{bmatrix}
$$

---

## 3. Transforming Rays

> [!WHY] 🤔 Wait, But Why? — In Module 1, we generated ray directions in *camera* space. But NeRF's neural network lives in *world* space — it has memorized the density and color of every point in the *world*. So before we can march our ray through the scene, we must rotate it into world coordinates.

**Ray direction** transforms with the rotation only (directions don't have a position):

$$
\mathbf{d}_{world} = R \cdot \mathbf{d}_{cam}
$$

**Ray origin** is simply the camera's position:

$$
\mathbf{o}_{world} = \mathbf{t}
$$

```python
def transform_ray_to_world(d_cam, c2w):
    R = c2w[:3, :3]     # 3x3 rotation
    t = c2w[:3, 3]      # 3x1 translation
    
    d_world = R @ d_cam  # rotate direction
    o_world = t           # camera position = ray origin
    return o_world, d_world
```

> [!CODE] 💻 Key insight: We multiply the direction by $R$ but NOT by $\mathbf{t}$. A direction vector doesn't have a position — it just points somewhere. Translation would change *where* the arrow is, not *which way* it points.

---

## 4. Why NeRF Needs Multiple Cameras

The entire point of NeRF is to combine information from **many cameras** (many different $c2w$ matrices). Each camera sees the scene from a different angle. By shooting rays from all these cameras into the same world space and comparing the rendered pixels to the actual photos, NeRF learns the 3D structure.

> [!WARNING] ⚠️ Common Mistake: Confusing $c2w$ (camera-to-world) with $w2c$ (world-to-camera). They are inverses of each other! NeRF datasets typically provide $c2w$ because it's more intuitive: "where is this camera in the world?"

---

## 5. Experiment

Use the visualizer on the right to explore 3D transformations:

1. **Translation** ($t_x, t_y, t_z$): Move the camera around the world. Watch the colored axes move with it.
2. **Rotation** (Pitch, Yaw, Roll): Rotate the camera's orientation. Watch how the frustum (the trapezoid showing the camera's field of view) changes direction.
3. Notice that the **World axes** (dashed) never move — only the camera axes do.

> [!CHALLENGE] 🏋️ Thought Experiment: If you have two cameras pointing at the same object from opposite sides, their $c2w$ matrices will have translations on opposite sides of the object and rotations that differ by ~180° in yaw. Can you set up the visualizer to show this?
