import numpy as np

class CameraSimulator:
    def __init__(self, fx, fy, cx, cy, img_w, img_h):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.img_w = img_w
        self.img_h = img_h

    def get_intrinsic_matrix(self):
        return np.array([
            [self.fx, 0,       self.cx],
            [0,       self.fy, self.cy],
            [0,       0,       1      ]
        ])

    def project_point(self, X_c, Y_c, Z_c):
        """
        Projects a 3D point in camera coordinates onto the 2D image plane.
        """
        if Z_c >= 0:
            return None # Behind camera or at center (assuming looking down -Z)
            
        # Pinhole projection
        x = (self.fx * X_c) / abs(Z_c) + self.cx
        y = (self.fy * Y_c) / abs(Z_c) + self.cy
        
        return (x, y)

    def generate_ray(self, u, v):
        """
        Generates a 3D ray direction vector from a 2D pixel coordinate (u, v).
        Using OpenGL convention (camera looks down -Z, Y is up, X is right).
        """
        dir_x = (u - self.cx) / self.fx
        dir_y = -(v - self.cy) / self.fy
        dir_z = -1.0
        
        # Normalize
        direction = np.array([dir_x, dir_y, dir_z])
        direction = direction / np.linalg.norm(direction)
        
        return direction
