# NeRF_Edu 🌟

**Interactive Neural Radiance Fields (NeRF) Educational Sandbox**

NeRF_Edu is a stunning, interactive web application built with Python and Streamlit, designed to demystify the complex mathematics and architecture behind Neural Radiance Fields (NeRFs). It serves as both a high-fidelity visual sandbox and an educational walkthrough for students, researchers, and AI enthusiasts.

---

## 🎨 Features & Modules

The application is structured into an immersive, modular journey:

1. **Introduction to NeRF**: High-level conceptual overview explaining how 2D images are transformed into a continuous 3D volumetric scene using Multi-Layer Perceptrons (MLPs).
2. **Ray Casting & 3D Geometry**: Interactive 3D plots demonstrating how rays are cast from the camera origin through screen pixels into the 3D scene.
3. **Positional Encoding**: A deep-dive interactive widget into the high-frequency sine/cosine encoding trick that allows MLPs to learn sharp, high-resolution details.
4. **Volume Rendering Math**: Explores the physics of light transport, integration, and the exact continuous integrals approximated by discrete sampling in NeRFs.
5. **Interactive Training Sandbox**: A mock training loop demonstrating how loss (MSE) drops over time and how the rendered image iteratively improves and sharpens.

### UI/UX Design
The application features a gorgeous, custom dark-mode aesthetic with:
- Glassmorphism UI elements and glowing gradients.
- Interactive Plotly 3D visualizers.
- Custom CSS injected directly into Streamlit for a premium, app-like feel.

---

## 🚀 Setup & Installation

### Prerequisites
- **Python 3.9+**
- **pip** package manager

### Running Locally

1. **Clone the repository**
   ```bash
   git clone git@github.com:Shyam-SN/NeRF_Edu.git
   cd NeRF_Edu
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   The application requires Streamlit, Plotly, NumPy, and Pandas.
   ```bash
   pip install streamlit plotly numpy pandas
   ```

4. **Launch the Web App**
   ```bash
   streamlit run app/main.py
   ```

5. **Explore**
   Open your browser to `http://localhost:8501` and start learning!

---

## 🧠 Educational Goals
NeRF_Edu was built with the belief that complex AI concepts are best understood through interactive visualization. By allowing users to physically drag camera rays, tweak positional encoding frequencies, and watch simulated training loops, the abstract math of Neural Rendering becomes highly intuitive.
