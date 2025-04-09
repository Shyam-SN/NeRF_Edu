import numpy as np

def generate_ray_samples(origin, direction, near, far, n_samples, stratified=False):
    """
    Generates N sample points along a ray.
    origin: (3,) array
    direction: (3,) normalized array
    near: float
    far: float
    n_samples: int
    stratified: bool (if True, applies random jitter within bins)
    """
    # Create N evenly spaced bins
    t_vals = np.linspace(0., 1., n_samples)
    z_vals = near * (1. - t_vals) + far * t_vals
    
    if stratified:
        # Get bin sizes
        mids = 0.5 * (z_vals[1:] + z_vals[:-1])
        upper = np.concatenate([mids, [z_vals[-1]]])
        lower = np.concatenate([[z_vals[0]], mids])
        
        # Random sample within each bin
        t_rand = np.random.rand(n_samples)
        z_vals = lower + (upper - lower) * t_rand
        
    # r(t) = o + t * d
    # Broadcasting: (3,) + (N, 1) * (3,) -> (N, 3)
    pts = origin + z_vals[:, np.newaxis] * direction
    
    return pts, z_vals
