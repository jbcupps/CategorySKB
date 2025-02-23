from flask import Flask, render_template, send_from_directory, request
from pathlib import Path
import os
from dotenv import load_dotenv
from .errors import register_error_handlers
from .logging_config import setup_logging
import numpy as np
from src.topology import Point4D, rotation_matrix_4d, apply_transformation, Tetrahedron4D
from src.visualization import project_to_3d, plot_3d_projection # Import necessary functions
import matplotlib
matplotlib.use('Agg') # Use the Agg backend for rendering to a file
import io, base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__,
                static_url_path='',
                static_folder=Path(__file__).parent / 'static',
                template_folder=Path(__file__).parent / 'templates')

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'skb.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up logging
    setup_logging(app)

    # Register error handlers
    register_error_handlers(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/modeler')
    def modeler():
        app.logger.info('Serving modeler page')
        return render_template('modeler.html')

    @app.route('/analysis')
    def analysis():
        app.logger.info('Serving analysis page')
        return render_template('analysis.html')

    @app.route('/plot_tetrahedron', methods=['GET', 'POST'])
    def plot_tetrahedron_route():
        # Default tetrahedron
        p1 = Point4D(1, 0, 0, 0)
        p2 = Point4D(0, 1, 0, 0)
        p3 = Point4D(0, 0, 1, 0)
        p4 = Point4D(0, 0, 0, 1)
        tetra = Tetrahedron4D([p1, p2, p3, p4])
        edges = [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (1, 3), (2, 3)
        ]

        if request.method == 'POST':
            # Get rotation parameters from the form
            angle = float(request.form.get('angle', 0))  # Default to 0 if not provided
            plane = request.form.get('plane', 'xy')       # Default to 'xy' if not provided

            # Rotate the tetrahedron
            rotation = rotation_matrix_4d(angle, plane=plane)
            rotated_vertices = [apply_transformation(v, rotation) for v in tetra.vertices]
            tetra = Tetrahedron4D(rotated_vertices)

        # Generate the plot
        projected_points = [project_to_3d(p) for p in tetra.vertices]
        x = [p[0] for p in projected_points]
        y = [p[1] for p in projected_points]
        z = [p[2] for p in projected_points]

        fig = Figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z)

        if edges:
            for edge in edges:
                p1_proj = projected_points[edge[0]]
                p2_proj = projected_points[edge[1]]
                ax.plot([p1_proj[0], p2_proj[0]], [p1_proj[1], p2_proj[1]], [p1_proj[2], p2_proj[2]], 'k-')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("Tetrahedron Projection")

        # Convert plot to a base64 encoded image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

        return render_template('index.html', image=pngImageB64String)

    # Register blueprints here
    from . import skb
    app.register_blueprint(skb.bp)
    app.logger.info('Registered SKB blueprint')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)