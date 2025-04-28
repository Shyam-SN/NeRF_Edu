import numpy as np

def compute_volume_rendering_weights(sigmas, dists):
    """
    Computes alpha, transmittance, and final rendering weights 
    given volume densities (sigmas) and distances between samples (dists).
    
    sigmas: (N,) array of densities
    dists: (N,) array of distance to next sample (delta_i)
    """
    
    # 1. Compute Alpha
    # alpha = 1 - exp(-sigma * delta)
    alphas = 1.0 - np.exp(-sigmas * dists)
    
    # 2. Compute Transmittance
    # T_i = prod_{j=1}^{i-1} (1 - alpha_j)
    # Using cumprod. The first sample always has T=1.0.
    # To do this cleanly: prepend 1.0 to (1 - alpha), compute cumprod, and drop the last element.
    ones = np.array([1.0])
    one_minus_alphas = 1.0 - alphas
    
    # T_0 = 1.0, T_1 = (1-a_0), T_2 = (1-a_0)(1-a_1), etc.
    transmittances = np.cumprod(np.concatenate([ones, one_minus_alphas]))[:-1]
    
    # 3. Compute final weights
    # w_i = T_i * alpha_i
    weights = transmittances * alphas
    
    return alphas, transmittances, weights
