from typing import Dict, Tuple, List
import numpy as np
from skb import SKB, create_particle, PARTICLE_CONFIGS
from config import Config

class ParticleData:
    KNOWN_PARTICLES = {
        'proton': {'mass': 938.272, 'charge': 1.0},
        'neutron': {'mass': 939.565, 'charge': 0.0},
        'pion_plus': {'mass': 139.570, 'charge': 1.0},
        'electron': {'mass': 0.511, 'charge': -1.0},
        'muon': {'mass': 105.658, 'charge': -1.0}
    }

class ModelAnalyzer:
    def __init__(self, 
                 gamma: float = Config.DEFAULT_GAMMA, 
                 delta: float = Config.DEFAULT_DELTA, 
                 epsilon: float = Config.DEFAULT_EPSILON):
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
    
    def create_all_particles(self) -> Dict[str, SKB]:
        return {
            name: create_particle(name, config['twist_numbers'], config['linking_pairs'])
            for name, config in PARTICLE_CONFIGS.items()
        }
    
    def analyze_particle(self, name: str, skb: SKB) -> Dict:
        if name not in ParticleData.KNOWN_PARTICLES:
            return {'name': name, 'error': f"No experimental data for {name}"}
        
        actual = ParticleData.KNOWN_PARTICLES[name]
        predicted_charge = skb.get_charge()
        predicted_mass = skb.get_mass(self.gamma, self.delta, self.epsilon)
        
        return {
            'name': name,
            'predicted_charge': predicted_charge,
            'actual_charge': actual['charge'],
            'charge_error': abs(predicted_charge - actual['charge']),
            'predicted_mass': predicted_mass,
            'actual_mass': actual['mass'],
            'mass_error': abs(predicted_mass - actual['mass']),
            'mass_error_percent': 100 * abs(predicted_mass - actual['mass']) / actual['mass']
        }
    
    def analyze_all_particles(self) -> List[Dict]:
        particles = self.create_all_particles()
        return [self.analyze_particle(name, skb) for name, skb in particles.items()]
    
    def fit_mass_parameters(self) -> Tuple[float, float, float]:
        particles = self.create_all_particles()
        A = np.array([
            [len(particles['electron'].sub_skbs), 
             particles['electron'].get_total_linking_number(), 1],
            [len(particles['proton'].sub_skbs), 
             particles['proton'].get_total_linking_number(), 1],
            [len(particles['pion_plus'].sub_skbs), 
             particles['pion_plus'].get_total_linking_number(), 1]
        ])
        b = np.array([
            ParticleData.KNOWN_PARTICLES['electron']['mass'],
            ParticleData.KNOWN_PARTICLES['proton']['mass'],
            ParticleData.KNOWN_PARTICLES['pion_plus']['mass']
        ])
        gamma, delta, epsilon = np.linalg.solve(A, b)
        return gamma, delta, epsilon