# 🌫️ Module 5: Volume Rendering

We've learned to shoot rays and sample points along them (Module 4). Now comes the million-dollar question: **how do we turn a bunch of density and color values into a single pixel color?**

---

## 1. The Beer-Lambert Law

> [!ANALOGY] 🌫️ The Fog Machine at a Concert: You're at a live concert. The fog machine is blasting. You can *barely* see the guitarist through the thick haze. The Beer-Lambert Law is literally quantifying how badly the fog machine ruined your view. It says: the probability that a photon survives through fog decays *exponentially* with distance. A little fog? You can see through. A LOT of fog? You can't see your own hand.

Let $\sigma(\mathbf{x})$ be the **Volume Density** at a point — the probability per unit distance that a photon gets absorbed or scattered.

- $\sigma = 0$ → empty air (photon flies right through)
- $\sigma = \infty$ → solid rock (photon is immediately absorbed)

The **Transmittance** $T(t)$ is the probability that a photon travels from the camera to depth $t$ without hitting *anything*:

$$
T(t) = \exp\left(-\int_0^t \sigma(\mathbf{r}(s))\, ds\right)
$$

> [!AHA] Transmittance is always between 0 and 1. It starts at $T(0) = 1$ (nothing has blocked us yet) and decreases monotonically as we encounter more and more density. If there's a solid wall at $t = 3$, then $T(t)$ drops to ~0 for all $t > 3$. Everything behind the wall is invisible — that's occlusion!

---

## 2. The Volume Rendering Integral

To get the final pixel color, we integrate along the entire ray. At each point $t$, we consider:

1. **$\mathbf{c}(t)$** — What color is emitted here?
2. **$\sigma(t)$** — How dense is the material here? (probability of stopping)
3. **$T(t)$** — Can the camera even *see* this point? (has light been blocked?)

The **Volume Rendering Integral**:

$$
C(\mathbf{r}) = \int_{t_{near}}^{t_{far}} T(t) \cdot \sigma(\mathbf{r}(t)) \cdot \mathbf{c}(\mathbf{r}(t), \mathbf{d})\, dt
$$

> [!WHY] 🤔 Wait, But Why? — This equation is the mathematical core of NeRF. It says: "the final color of a pixel is the sum of all the colors along the ray, weighted by how likely we are to actually hit each point AND how likely it is that nothing in front has already blocked our view." It elegantly handles transparency, occlusion, fog, and solid surfaces — all in one equation.

---

## 3. Discretization: Alpha Compositing

We can't compute continuous integrals on a computer. Instead, we use our $N$ discrete samples from Module 4.

Let $\delta_i = t_{i+1} - t_i$ (the distance between consecutive samples).

**Alpha** is the discrete probability of stopping at sample $i$:

$$
\alpha_i = 1 - \exp(-\sigma_i \cdot \delta_i)
$$

- $\sigma_i = 0$ (empty air) → $\alpha_i = 0$ (nothing here)
- $\sigma_i = \infty$ (solid wall) → $\alpha_i = 1$ (definitely stops here)

**Transmittance** is the product of "not hitting anything" at all previous samples:

$$
T_i = \prod_{j=1}^{i-1}(1 - \alpha_j)
$$

**Rendering Weight** combines both:

$$
w_i = T_i \cdot \alpha_i
$$

**Final color** is the weighted sum:

$$
\hat{C}(\mathbf{r}) = \sum_{i=1}^{N} w_i \cdot \mathbf{c}_i
$$

```python
def volume_render(sigmas, colors, dists):
    """
    sigmas: (N,) density at each sample
    colors: (N, 3) RGB color at each sample  
    dists:  (N,) distance between consecutive samples
    """
    # Alpha: probability of stopping at each sample
    alphas = 1.0 - np.exp(-sigmas * dists)
    
    # Transmittance: cumulative product of (1 - alpha)
    T = np.cumprod(np.concatenate([[1.0], 1.0 - alphas]))[:-1]
    
    # Rendering weights
    weights = T * alphas  # shape: (N,)
    
    # Final pixel color
    pixel_color = np.sum(weights[:, None] * colors, axis=0)  # shape: (3,)
    return pixel_color
```

> [!AHA] The weights $w_i$ always sum to ≤ 1 (they sum to exactly 1 if the ray hits something solid). If the ray passes through empty space entirely, all weights are 0 and the pixel is black (or background color). This is physically correct — if there's nothing in the scene, you see nothing!

---

## 4. The Occlusion Principle

The transmittance $T_i$ is the key to realistic rendering. Consider:

- **Sample 1** has very high density (a wall) → $\alpha_1 \approx 1$
- **$T_2 = 1 - \alpha_1 \approx 0$** → Sample 2's weight is nearly zero
- Everything *behind* the wall is invisible!

This is exactly how the real world works. You can't see through solid objects. NeRF learns this naturally because the math enforces it.

> [!WARNING] ⚠️ Common Bug: If you forget to compute transmittance and just average the colors, you get a ghostly transparent world where you can see through walls. The transmittance term is what makes opaque surfaces opaque.

---

## 5. Experiment

Use the visualizer on the right with 4 discrete sample points:

1. Set **Sample 1** density to maximum — watch Samples 2, 3, 4 get completely blocked (their weights drop to 0).
2. Set all densities to low values — notice the weights are more evenly distributed (semi-transparent fog).
3. Set only **Sample 3** to high density — Samples 1 and 2 contribute their colors, but Sample 4 is occluded.

> [!CHALLENGE] 🏋️ Predict the Output: If Sample 1 has $\sigma_1 = 0$, Sample 2 has $\sigma_2 = 100$ (solid), and Samples 3-4 have $\sigma = 0$, what are the rendering weights? Answer: $w_1 = 0$, $w_2 \approx 1$, $w_3 = w_4 = 0$. The pixel color equals Sample 2's color exactly.
