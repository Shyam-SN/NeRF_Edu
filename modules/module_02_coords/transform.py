import numpy as np
from scipy.spatial.transform import Rotation

def create_c2w_matrix(tx, ty, tz, rx_deg, ry_deg, rz_deg):
    """
    Creates a 4x4 Camera-to-World (c2w) transformation matrix.
    Translation: tx, ty, tz
    Rotation (Euler angles in degrees): rx_deg, ry_deg, rz_deg
    """
    # Create 3x3 rotation matrix from Euler angles (XYZ convention)
    # Pitch (X), Yaw (Y), Roll (Z)
    rot = Rotation.from_euler('xyz', [rx_deg, ry_deg, rz_deg], degrees=True)
    R = rot.as_matrix()
    
    # 3x1 Translation vector
    t = np.array([tx, ty, tz])
    
    # Construct 4x4 homogeneous matrix
    c2w = np.eye(4)
    c2w[:3, :3] = R
    c2w[:3, 3] = t
    
    return c2w

def transform_point(c2w, point_cam):
    """
    Transforms a 3D point from Camera Space to World Space.
    point_cam: (3,) array
    """
    # Make homogeneous (x, y, z, 1)
    point_cam_h = np.append(point_cam, 1.0)
    
    # Multiply
    point_world_h = c2w @ point_cam_h
    
    # Return (x, y, z)
    return point_world_h[:3]

def transform_vector(c2w, vector_cam):
    """
    Transforms a direction vector from Camera Space to World Space.
    vector_cam: (3,) array
    """
    R = c2w[:3, :3]
    return R @ vector_cam
