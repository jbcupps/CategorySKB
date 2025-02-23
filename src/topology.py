import numpy as np

class Point4D:
    def __init__(self, x, y, z, w):
        self.coords = np.array([x, y, z, w])

    def __repr__(self):
        return f"Point4D({self.coords[0]}, {self.coords[1]}, {self.coords[2]}, {self.coords[3]})"

class Simplex4D: #Abstract class
    def __init__(self, vertices):
        if not all(isinstance(v, Point4D) for v in vertices):
            raise TypeError("Vertices must be Point4D objects")
        self.vertices = vertices

class LineSegment4D(Simplex4D):
    def __init__(self, vertices):
        if len(vertices)!=2:
            raise ValueError("Line segment requires 2 vertices")
        super().__init__(vertices)
class Triangle4D(Simplex4D):
    def __init__(self, vertices):
        if len(vertices)!=3:
            raise ValueError("Triangle requires 3 vertices")
        super().__init__(vertices)

class Tetrahedron4D(Simplex4D):
    def __init__(self, vertices):
        if len(vertices)!=4:
            raise ValueError("Tetrahedron requires 4 vertices")
        super().__init__(vertices)
class Pentachoron4D(Simplex4D):
    def __init__(self, vertices):
        if len(vertices)!=5:
            raise ValueError("Pentachoron requires 5 vertices")
        super().__init__(vertices)

# Example usage
p1 = Point4D(1, 0, 0, 0)
p2 = Point4D(0, 1, 0, 0)
p3 = Point4D(0, 0, 1, 0)
p4 = Point4D(0, 0, 0, 1)
p5 = Point4D(0.25,0.25,0.25,0.25)

tetra = Tetrahedron4D([p1,p2,p3,p4])
penta = Pentachoron4D([p1,p2,p3,p4,p5])
line = LineSegment4D([p1, p2])

def rotation_matrix_4d(angle, plane="xy"):
    """
    Generates a 4D rotation matrix for a given angle and plane.

    Args:
        angle: The angle of rotation in radians.
        plane: The plane of rotation ("xy", "xz", "xw", "yz", "yw", "zw").
               Planes are defined by pairs of coordinate axes.

    Returns:
        A 4x4 NumPy array representing the rotation matrix.
    """
    c = np.cos(angle)
    s = np.sin(angle)
    matrix = np.eye(4)  # Start with the identity matrix

    if plane == "xy":
        matrix[0, 0] = c
        matrix[0, 1] = -s
        matrix[1, 0] = s
        matrix[1, 1] = c
    elif plane == "xz":
        matrix[0, 0] = c
        matrix[0, 2] = -s
        matrix[2, 0] = s
        matrix[2, 2] = c
    elif plane == "xw":
        matrix[0, 0] = c
        matrix[0, 3] = -s
        matrix[3, 0] = s
        matrix[3, 3] = c
    elif plane == "yz":
        matrix[1, 1] = c
        matrix[1, 2] = -s
        matrix[2, 1] = s
        matrix[2, 2] = c
    elif plane == "yw":
        matrix[1, 1] = c
        matrix[1, 3] = -s
        matrix[3, 1] = s
        matrix[3, 3] = c
    elif plane == "zw":
        matrix[2, 2] = c
        matrix[2, 3] = -s
        matrix[3, 2] = s
        matrix[3, 3] = c
    else:
        raise ValueError("Invalid plane of rotation")

    return matrix

def apply_transformation(point, matrix):
    """Applies a 4x4 transformation matrix to a Point4D."""
    if not isinstance(point, Point4D):
        raise TypeError("point must be a Point4D object")
    if not isinstance(matrix, np.ndarray) or matrix.shape != (4, 4):
        raise TypeError("matrix must be a 4x4 NumPy array")

    transformed_coords = np.dot(matrix, point.coords)
    return Point4D(*transformed_coords)

# Example Usage:
rotation = rotation_matrix_4d(np.pi / 2, plane="xy")  # Rotate 90 degrees in the xy-plane
p2 = apply_transformation(p1, rotation)
print(p2)  # Output: Point4D(6.123233995736766e-17, 1.0, 0.0, 0.0) (approximately (0, 1, 0, 0)) 