from flask import Flask, render_template, request, jsonify
from datetime import datetime
from analysis import ModelAnalyzer, ParticleData
from skb import SKB, SubSKB, create_particle, PARTICLE_CONFIGS
import numpy as np

app = Flask(__name__)

# Global analyzer instance (stateful for parameter adjustments)
analyzer = ModelAnalyzer()

@app.route('/')
def index():
    """Render the main interface."""
    return render_template('index.html', 
                         particles=PARTICLE_CONFIGS.keys(),
                         date=datetime.now().strftime("%B %d, %Y"))

@app.route('/analyze_all', methods=['GET'])
def analyze_all():
    """Analyze all predefined particles."""
    try:
        results = analyzer.analyze_all_particles()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/analyze_particle', methods=['POST'])
def analyze_particle():
    """Analyze a specific predefined particle."""
    try:
        particle_name = request.json.get('particle_name')
        if particle_name not in PARTICLE_CONFIGS:
            return jsonify({'error': f"Unknown particle: {particle_name}"})
        config = PARTICLE_CONFIGS[particle_name]
        skb = create_particle(particle_name, config['twist_numbers'], config['linking_pairs'])
        result = analyzer.analyze_particle(particle_name, skb)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/analyze_custom', methods=['POST'])
def analyze_custom():
    """Analyze a custom SKB configuration."""
    try:
        data = request.json
        twist_numbers = [int(t) for t in data.get('twist_numbers', [])]
        linking_pairs = [(int(p['i']), int(p['j']), int(p['value'])) 
                        for p in data.get('linking_pairs', [])]
        particle_name = data.get('particle_name', 'custom')
        
        sub_skbs = [SubSKB(t) for t in twist_numbers]
        skb = SKB(sub_skbs)
        for i, j, value in linking_pairs:
            skb.set_linking_number(i, j, value)
        result = analyzer.analyze_particle(particle_name, skb)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/fit_parameters', methods=['POST'])
def fit_parameters():
    """Fit mass parameters and update analyzer."""
    try:
        global analyzer
        gamma, delta, epsilon = analyzer.fit_mass_parameters()
        analyzer = ModelAnalyzer(gamma, delta, epsilon)
        return jsonify({'gamma': gamma, 'delta': delta, 'epsilon': epsilon})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/update_parameters', methods=['POST'])
def update_parameters():
    """Manually update mass parameters."""
    try:
        global analyzer
        gamma = float(request.json.get('gamma', analyzer.gamma))
        delta = float(request.json.get('delta', analyzer.delta))
        epsilon = float(request.json.get('epsilon', analyzer.epsilon))
        analyzer = ModelAnalyzer(gamma, delta, epsilon)
        return jsonify({'gamma': gamma, 'delta': delta, 'epsilon': epsilon})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)