import numpy as np

def simulate_mlp(pts):
    """
    Simulates a trained NeRF MLP. 
    Instead of running a PyTorch model, we use a mathematical function 
    to represent a 3D sphere so we can render it in real-time on CPU.
    
    pts: (N, 3) array of 3D coordinates
    Returns:
        sigmas: (N,) array of densities
        colors: (N, 3) array of RGB colors
    """
    # Sphere properties
    center = np.array([0.0, 0.0, 4.0])
    radius = 1.0
    
    # Distance from center
    dist = np.linalg.norm(pts - center, axis=-1)
    
    # Density: High if inside the sphere, 0 otherwise
    # We use a soft sigmoid-like dropoff for smoother rendering
    sigmas = np.where(dist < radius, 50.0 * (radius - dist), 0.0)
    
    # Color: Calculate surface normal for basic lighting
    # Normal is just the normalized vector from center to point
    normals = (pts - center) / (dist[:, np.newaxis] + 1e-6)
    
    # Light coming from top right
    light_dir = np.array([1.0, 1.0, -1.0])
    light_dir = light_dir / np.linalg.norm(light_dir)
    
    # Diffuse lighting (dot product)
    diffuse = np.maximum(0.0, np.sum(normals * light_dir, axis=-1))
    
    # Base color is red [1, 0, 0]
    base_color = np.array([1.0, 0.2, 0.2])
    ambient = 0.2
    
    # Final color for each point (N, 3)
    intensity = (ambient + 0.8 * diffuse)[:, np.newaxis]
    colors = base_color * intensity
    colors = np.clip(colors, 0.0, 1.0)
    
    return sigmas, colors

def render_pixel(u, v, W, H, f, c2w, near, far, n_samples):
    """
    Executes the full NeRF pipeline for a single pixel.
    """
    # 1. Camera Math: Pixel to Ray Direction (Camera Space)
    # x = (u - cx) / f, y = -(v - cy) / f (OpenGL y-down)
    cx, cy = W / 2.0, H / 2.0
    dir_c = np.array([(u - cx) / f, -(v - cy) / f, -1.0])
    dir_c = dir_c / np.linalg.norm(dir_c)
    
    # 2. Camera to World Space
    # c2w is 4x4. Extract rotation 3x3 and translation 3x1
    R = c2w[:3, :3]
    t = c2w[:3, 3]
    
    origin = t
    direction = R @ dir_c
    
    # 3. Ray Marching (Uniform samples for speed)
    t_vals = np.linspace(near, far, n_samples)
    pts = origin + t_vals[:, np.newaxis] * direction
    
    # 4. Query MLP (Simulated)
    sigmas, colors = simulate_mlp(pts)
    
    # 5. Volume Rendering
    dists = np.diff(t_vals)
    dists = np.append(dists, 1e10) # Last interval is infinity
    
    alphas = 1.0 - np.exp(-sigmas * dists)
    
    ones = np.array([1.0])
    one_minus_alphas = 1.0 - alphas
    transmittances = np.cumprod(np.concatenate([ones, one_minus_alphas]))[:-1]
    
    weights = transmittances * alphas
    
    # Sum up colors along the ray
    final_color = np.sum(weights[:, np.newaxis] * colors, axis=0)
    
    return final_color
