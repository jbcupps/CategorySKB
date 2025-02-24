import unittest
import numpy as np
from skb.models import Point4D, rotation_matrix_4d, apply_transformation, Tetrahedron4D, LineSegment4D, Triangle4D, Pentachoron4D

class TestTopology(unittest.TestCase):

    def test_point4d_creation(self):
        p = Point4D(1, 2, 3, 4)
        self.assertTrue(np.array_equal(p.coords, np.array([1, 2, 3, 4])))

    def test_rotation_matrix_xy(self):
        angle = np.pi / 2
        expected_matrix = np.array([
            [0, -1, 0, 0],
            [1,  0, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]
        ])
        rotation_matrix = rotation_matrix_4d(angle, plane="xy")
        self.assertTrue(np.allclose(rotation_matrix, expected_matrix))

    def test_apply_transformation(self):
        p = Point4D(1, 0, 0, 0)
        rotation = rotation_matrix_4d(np.pi / 2, plane="xy")
        p_rotated = apply_transformation(p, rotation)
        expected_coords = np.array([0, 1, 0, 0])
        self.assertTrue(np.allclose(p_rotated.coords, expected_coords))

    def test_tetrahedron_creation(self):
        p1 = Point4D(1, 0, 0, 0)
        p2 = Point4D(0, 1, 0, 0)
        p3 = Point4D(0, 0, 1, 0)
        p4 = Point4D(0, 0, 0, 1)
        tetra = Tetrahedron4D([p1, p2, p3, p4])
        self.assertEqual(len(tetra.vertices), 4)

    def test_invalid_simplex_vertices(self):
        with self.assertRaises(TypeError):
            LineSegment4D([1,2])
        with self.assertRaises(ValueError):
            LineSegment4D([Point4D(1,0,0,0)])
        with self.assertRaises(ValueError):
            Triangle4D([Point4D(1,0,0,0)])
        with self.assertRaises(ValueError):
            Tetrahedron4D([Point4D(1,0,0,0)])
        with self.assertRaises(ValueError):
            Pentachoron4D([Point4D(1,0,0,0)])

if __name__ == '__main__':
    unittest.main() 