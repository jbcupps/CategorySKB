from flask import Flask, render_template, request, jsonify
import numpy as np
from .models import Point4D, rotation_matrix_4d, apply_transformation, Tetrahedron4D
from .views import project_to_3d, plot_3d_projection
import matplotlib
matplotlib.use('Agg')
import io, base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from .errors import register_error_handlers
from .logging_config import setup_logging

app = Flask(__name__)

# Default configuration (you might move this to a config.py file)
app.config.from_mapping(
    SECRET_KEY='dev',  # Change this in production!
)

# Set up logging
setup_logging(app)

# Register error handlers
register_error_handlers(app)

@app.route('/')
def index():
    return render_template('index.html')

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
        # Get rotation parameters
        angle = float(request.form.get('angle', 0))
        plane = request.form.get('plane', 'xy')

        # Rotate
        rotation = rotation_matrix_4d(angle, plane=plane)
        rotated_vertices = [apply_transformation(v, rotation) for v in tetra.vertices]
        tetra = Tetrahedron4D(rotated_vertices)

    # Generate plot
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

    # Convert to base64
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    return render_template('index.html', image=pngImageB64String)

@app.route('/analysis')
def analysis_route():
    return render_template('analysis.html')

@app.route('/modeler', methods=['GET', 'POST']) #Allow post requests
def modeler_route():
    step = request.args.get('step', 1, type=int)  # Get step from query parameter, default to 1
    tutorial_mode = request.args.get('tutorial', 'false').lower() == 'true' # Convert to boolean
    return render_template('modeler.html', step=step, tutorial_mode=tutorial_mode)

@app.route('/validate_quark', methods=['POST'])
def validate_quark():
    data = request.get_json()

    # --- Your SKB model calculations go here ---
    # This is just placeholder logic; replace with your actual calculations
    generation = int(data.get('generation', 1))
    color = data.get('color', 'red')
    twist_number = int(data.get('twist_number', 0))
    linking_pairs = data.get('linking_pairs', [])

    # Example calculations (replace with your model)
    charge = 0
    if twist_number > 0:
        charge = 2/3
    elif twist_number < 0:
        charge = -1/3

    mass = generation * 10  # Very simplistic example
    spin = 1/2

    return jsonify({
        'charge': charge,
        'mass': mass,
        'spin': spin
    }) 