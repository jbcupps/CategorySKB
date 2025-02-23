from flask import Flask, render_template, request, jsonify
from datetime import datetime
from analysis import ModelAnalyzer, ParticleData
from skb import SKB, SubSKB, create_particle, PARTICLE_CONFIGS, validate_sub_skb

app = Flask(__name__)
analyzer = ModelAnalyzer()

@app.route('/')
def index():
    return render_template('index.html', date="February 23, 2025")

@app.route('/analysis')
def analysis():
    return render_template('analysis.html', particles=PARTICLE_CONFIGS.keys(), date="February 23, 2025")

@app.route('/modeler')
def modeler():
    return render_template('modeler.html', date="February 23, 2025")

@app.route('/analyze_all', methods=['GET'])
def analyze_all():
    results = analyzer.analyze_all_particles()
    return jsonify(results)

@app.route('/analyze_custom', methods=['POST'])
def analyze_custom():
    data = request.json
    twist_numbers = data.get('twist_numbers', [])
    linking_pairs = data.get('linking_pairs', [])
    particle_name = data.get('particle_name', 'custom')
    sub_skbs = [SubSKB(t) for t in twist_numbers]
    skb = SKB(sub_skbs)
    for pair in linking_pairs:
        skb.set_linking_number(pair['i'], pair['j'], pair['value'])
    result = analyzer.analyze_particle(particle_name, skb)
    return jsonify(result)

@app.route('/fit_parameters', methods=['POST'])
def fit_parameters():
    global analyzer
    gamma, delta, epsilon = analyzer.fit_mass_parameters()
    analyzer = ModelAnalyzer(gamma, delta, epsilon)
    return jsonify({'gamma': gamma, 'delta': delta, 'epsilon': epsilon})

@app.route('/update_parameters', methods=['POST'])
def update_parameters():
    global analyzer
    data = request.json
    gamma = float(data.get('gamma', analyzer.gamma))
    delta = float(data.get('delta', analyzer.delta))
    epsilon = float(data.get('epsilon', analyzer.epsilon))
    analyzer = ModelAnalyzer(gamma, delta, epsilon)
    return jsonify({'gamma': gamma, 'delta': delta, 'epsilon': epsilon})

@app.route('/validate_quark', methods=['POST'])
def validate_quark():
    data = request.json
    sub_skb = SubSKB(data['twist_number'], data['generation'], data['color'])
    result = validate_sub_skb(sub_skb, data['quark'], analyzer.gamma, analyzer.epsilon)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)