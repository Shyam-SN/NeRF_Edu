# 🔦 Module 4: Ray Tracing and Sampling

We now know how to build a camera (Module 1), place it in the world (Module 2), and understand the math of space (Module 3). Time to fire lasers into the void.

---

## 1. What Is a Ray?

> [!ANALOGY] 🔫 Pixel Pew Pew: In real life, photons fly from the sun → bounce off objects → enter your eye. In NeRF, we skip all that chaos and reverse the process: we shoot lasers out of our eyeballs like Superman. Each pixel on the screen gets its own personal laser beam. We then taste-test the 3D space at regular intervals along each laser to figure out what color and density exists there.

A camera sensor is a grid of pixels. For each pixel, we cast a **ray** — a mathematical laser beam — into the 3D scene.

---

## 2. The Math of a Ray

A ray is a **parametric 3D line**. It has an origin $\mathbf{o}$ (where the camera is) and a direction $\mathbf{d}$ (where it's pointing). Any point along the ray is:

$$
\mathbf{r}(t) = \mathbf{o} + t \cdot \mathbf{d}, \quad t \in [t_{near}, t_{far}]
$$

- $t$ = distance traveled along the ray (like an odometer)
- $t_{near}$ = where we start sampling (ignore stuff right against the lens)
- $t_{far}$ = where we stop (ignore stuff infinitely far away)

> [!AHA] This is one of the most elegant equations in all of computer graphics. With just an origin, a direction, and a scalar $t$, you can describe every point on an infinite line. When $t = 0$, you're at the camera. When $t = 5$, you're 5 units into the scene.

```python
def point_on_ray(origin, direction, t):
    return origin + t * direction

# Example: camera at [0,0,0], looking into scene
origin = np.array([0, 0, 0])
direction = np.array([0, 0, -1])  # looking down -Z

# Point 5 units deep:
p = point_on_ray(origin, direction, 5.0)  # → [0, 0, -5]
```

---

## 3. Discretization: Ray Marching

NeRF's neural network predicts density and color at individual 3D points. We can't query it at *infinite* points along the ray — we must **discretize** the ray into $N$ samples.

### Uniform Sampling

The simplest approach: divide $[t_{near}, t_{far}]$ into $N$ evenly spaced intervals:

$$
t_i = t_{near} + \frac{i}{N}(t_{far} - t_{near}), \quad i = 0, 1, \ldots, N-1
$$

> [!WARNING] ⚠️ The Aliasing Trap: If we always sample at the *exact same* distances, the neural network learns to cheat — it only places density at those specific locations and leaves everything in between empty. This creates stair-step artifacts (aliasing). Imagine a fence where you can only see through specific slats — you'd miss entire objects between the slats.

### Stratified Sampling (The Fix)

NeRF's clever trick: still divide into $N$ bins, but pick a **random point within each bin**:

$$
t_i \sim \mathcal{U}\left[t_{near} + \frac{i-1}{N}(t_{far} - t_{near}), \quad t_{near} + \frac{i}{N}(t_{far} - t_{near})\right]
$$

```python
def stratified_sample(near, far, n_samples):
    """Sample with random jitter within each bin."""
    bin_edges = np.linspace(near, far, n_samples + 1)
    
    # Random point within each bin
    t_vals = bin_edges[:-1] + np.random.rand(n_samples) * (bin_edges[1:] - bin_edges[:-1])
    return t_vals
```

> [!AHA] During training, the jitter means the network sees a *different* set of continuous points every iteration. Over thousands of iterations, it effectively sees the entire continuous ray. This forces it to learn a smooth, continuous representation instead of discrete "fences."

---

## 4. From Samples to 3D Points

Once we have our $t$ values, computing the actual 3D coordinates is trivial:

$$
\mathbf{x}_i = \mathbf{o} + t_i \cdot \mathbf{d}
$$

```python
# Generate N 3D points along a ray
t_vals = stratified_sample(near=2.0, far=6.0, n_samples=64)
pts = origin[None, :] + t_vals[:, None] * direction[None, :]  
# Shape: (64, 3) — 64 points, each with (x, y, z) coordinates
```

> [!WHY] 🤔 Wait, But Why? — These 64 points are exactly what gets fed into the neural network (Module 6). For each point, the MLP predicts a density $\sigma$ (is there solid stuff here?) and a color $(r, g, b)$ (what color is it?). Then Module 5's volume rendering blends them all together.

---

## 5. Experiment

Use the visualizer on the right to simulate ray marching:

1. Adjust **Number of Samples ($N$)** — watch the density of orange dots change along the ray.
2. Toggle **Stratified Sampling** on/off — with it OFF, the dots are rigid soldiers in a line. With it ON, they jitter randomly within their bins. Watch them dance!
3. Move the **Near/Far planes** — this controls the region of space we care about.

> [!CHALLENGE] 🏋️ Think About It: Why would NeRF benefit from **hierarchical sampling** (first do a coarse pass with 64 samples, then concentrate more samples where density is high)? Hint: most of the ray passes through empty air, so 90% of uniform samples are wasted.
