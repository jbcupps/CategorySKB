import unittest
from skb.app import app  # Import your Flask app
from skb.models import Point4D
import numpy as np

class TestViews(unittest.TestCase):

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the index route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check for successful response
        self.assertIn(b'4D Topology Visualization', response.data) #check that correct page is being rendered

    def test_plot_tetrahedron_get(self):
        """Test the GET request to /plot_tetrahedron."""
        response = self.app.get('/plot_tetrahedron')
        self.assertEqual(response.status_code, 200)
        # You might also check if the form is present in the HTML

    def test_plot_tetrahedron_post(self):
        """Test the POST request to /plot_tetrahedron."""
        response = self.app.post('/plot_tetrahedron', data={
            'angle': str(np.pi / 4),
            'plane': 'xy'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'data:image/png;base64,', response.data)  # Check for image data

    def test_project_to_3d(self):
        from skb.views import project_to_3d
        p = Point4D(1,2,3,4)
        projected = project_to_3d(p)
        self.assertTrue(np.array_equal(projected, np.array([1,2,3])))

if __name__ == '__main__':
    unittest.main() 