import numpy as np
import matplotlib.pyplot as plt
from .models import Point4D, rotation_matrix_4d, apply_transformation, Tetrahedron4D  # Relative import

def project_to_3d(point4d, projection_matrix=None):
    """
    Projects a 4D point to 3D using a simple perspective projection.

    Args:
        point4d: A Point4D object.
        projection_matrix: Optional 4x4 projection matrix.  If None, a default is used.

    Returns:
        A NumPy array representing the 3D coordinates (x, y, z).
    """
    if not isinstance(point4d, Point4D):
        raise TypeError("point4d must be a Point4D object")

    # Default projection: Simple perspective projection (dropping the w coordinate)
    if projection_matrix is None:
        projection_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0]
        ])

    projected_coords = np.dot(projection_matrix, point4d.coords)
    return projected_coords


def plot_3d_projection(points, edges=None, title="3D Projection"):
    """
    Plots a 3D projection of a set of 4D points.

    Args:
        points: A list of Point4D objects.
        edges: A list of tuples, where each tuple contains two indices
               representing an edge between two points in the 'points' list.
    """

    projected_points = [project_to_3d(p) for p in points]
    x = [p[0] for p in projected_points]
    y = [p[1] for p in projected_points]
    z = [p[2] for p in projected_points]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z)

    if edges:
        for edge in edges:
            p1 = projected_points[edge[0]]
            p2 = projected_points[edge[1]]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'k-') #k-: black, solid line

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

def plot_tetrahedron(tetrahedron, title="Tetrahedron 4D projection"):
    if not isinstance(tetrahedron, Tetrahedron4D):
        raise TypeError("Input must be a Tetrahedron4D object")

    # Define edges of the tetrahedron
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3), (2, 3)
    ]
    plot_3d_projection(tetrahedron.vertices, edges, title) 