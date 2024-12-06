# 🚀 Module 0: What is NeRF?

Welcome, explorer. You're about to learn one of the most mind-bending ideas in modern computer science: **how to teach a neural network to hallucinate photorealistic 3D scenes from a handful of 2D photos.**

---

## The One-Sentence Pitch

**NeRF (Neural Radiance Fields)** takes ~50 photos of a scene from different angles, trains a neural network to memorize the entire 3D world, and then lets you render *brand new* photorealistic views from angles *you never photographed*.

> [!ANALOGY] 📸 Instagram vs. NeRF: A photo is a flat postcard. NeRF is a hologram. With a photo, you're stuck with one viewpoint forever. With NeRF, you can fly a virtual camera anywhere in the scene and render what you'd see — even behind the sofa you never photographed.

---

## How Is This Even Possible?

Here's the key insight that makes NeRF work:

**Every 2D photo is actually a *slice* of 3D information.** When you take 50 photos of a coffee mug from different angles, you're not just collecting 50 flat images — you're implicitly encoding the full 3D geometry of that mug. If the handle is visible from the left photo but hidden from the right, there's only *one* 3D arrangement that explains both views consistently.

NeRF exploits this by training a neural network to find that single consistent 3D representation.

> [!AHA] The magic: NeRF doesn't store a 3D model (no meshes, no point clouds, no voxel grids). Instead, it stores the *entire 3D scene* as the weights of a neural network. The network *is* the scene. Ask it "what color and density exists at position (x, y, z)?" and it answers instantly.

---

## The NeRF Pipeline at a Glance

To render a single pixel, NeRF chains together 7 ideas. Each one is a module in this course:

| Step | Module | What Happens |
|------|--------|-------------|
| 1 | 📷 **Camera Math** | Convert a pixel coordinate (u, v) into a 3D ray direction |
| 2 | 🌍 **Coordinate Systems** | Transform the ray from camera space to world space using the extrinsics matrix |
| 3 | 📐 **Linear Algebra** | Understand why matrix multiplications are spatial transformations |
| 4 | 🔦 **Ray Tracing** | March along the ray, sampling N discrete points in 3D space |
| 5 | 🌊 **Positional Encoding** | Encode each 3D coordinate into a high-dimensional feature vector so the network can see sharp details |
| 6 | 🧠 **The MLP** | Feed the encoded coordinates into an 8-layer neural network → get density (σ) and color (r,g,b) |
| 7 | 🌫️ **Volume Rendering** | Blend all N samples along the ray using Beer-Lambert transmittance → one final pixel color |

**Repeat for every pixel in the image.** For an 800×800 image, that's 640,000 rays × 128 samples = **81,920,000 neural network queries** per frame. 🤯

> [!WHY] This course exists because NeRF sits at the intersection of **computer vision**, **3D graphics**, **deep learning**, and **physics**. Understanding it means understanding all four fields. Let's go.

---

## What You'll Be Able to Do After This Course

By the time you finish Module 8, you will:

1. ✅ **Understand every equation** in the original NeRF paper (not just memorize — *understand*)
2. ✅ **Implement a working ray tracer** from scratch using NumPy
3. ✅ **Train a tiny neural radiance field** live in the app using PyTorch
4. ✅ **See the spectral bias problem** with your own eyes and fix it with Positional Encoding
5. ✅ **Render a 3D sphere** using the full NeRF pipeline — camera → rays → MLP → volume rendering

> [!CHALLENGE] Your ultimate challenge: After finishing all 8 modules, try modifying Module 8's `pipeline.py` to render TWO spheres instead of one. If you can do that, you truly understand NeRF end-to-end.

---

## How to Use This App

- **Left Panel** → Module navigation. Click any module to jump to it.
- **Center Panel** → Theory. The math, intuition, and code behind each concept.
- **Right Panel** → Interactive experiments. Sliders, live training, and visualizations.

Start with Module 1 and work your way through. Each module builds on the previous one, like chapters in a story.

*Let's shoot some rays.* 🔦
