import numpy as np

def apply_transformation(matrix, points):
    """
    Applies a 2x2 transformation matrix to a set of 2D points.
    matrix: 2x2 numpy array
    points: 2xN numpy array
    """
    return matrix @ points

def get_eigenvectors(matrix):
    """
    Computes real eigenvectors for a 2x2 matrix.
    Returns a list of valid (real) eigenvectors and their eigenvalues.
    """
    try:
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
    except np.linalg.LinAlgError:
        return [], []
        
    real_eigenvectors = []
    real_eigenvalues = []
    
    # We only care about real eigenvectors for the visualizer
    for i in range(2):
        if np.isreal(eigenvalues[i]):
            real_eigenvalues.append(np.real(eigenvalues[i]))
            real_eigenvectors.append(np.real(eigenvectors[:, i]))
            
    return real_eigenvectors, real_eigenvalues
