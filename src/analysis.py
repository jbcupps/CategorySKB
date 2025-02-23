from typing import Dict, Tuple, List
import numpy as np
from skb import SKB, create_particle, PARTICLE_CONFIGS

class ParticleData:
    """Experimental particle data for comparison."""
    # Mass in MeV/c², charge in e
    KNOWN_PARTICLES = {
        'proton': {'mass': 938.272, 'charge': 1.0},
        'neutron': {'mass': 939.565, 'charge': 0.0},
        'pion_plus': {'mass': 139.570, 'charge': 1.0},
        'electron': {'mass': 0.511, 'charge': -1.0},
        'muon': {'mass': 105.658, 'charge': -1.0}
    }

class ModelAnalyzer:
    """Analyzes SKB model predictions against experimental data."""
    
    def __init__(self, gamma: float = 313.09, delta: float = -0.0, 
                 epsilon: float = 0.511):
        """
        Initialize with mass function parameters.
        Default values from initial fitting with electron mass.
        """
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
    
    def create_all_particles(self) -> Dict[str, SKB]:
        """Create SKB representations for all configured particles."""
        return {name: create_particle(name, config['twist_numbers'], config['linking_pairs'])
                for name, config in PARTICLE_CONFIGS.items()}
    
    def analyze_particle(self, name: str, skb: SKB) -> Dict:
        """
        Compare SKB model predictions with experimental data.
        
        Args:
            name (str): Particle name
            skb (SKB): SKB model of the particle
            
        Returns:
            Dict containing predicted and actual values, with errors
        """
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
        """Analyze all configured particles."""
        particles = self.create_all_particles()
        return [self.analyze_particle(name, skb) for name, skb in particles.items()]
    
    def fit_mass_parameters(self) -> Tuple[float, float, float]:
        """
        Fit mass function parameters using experimental data.
        Uses a system of equations for electron, proton, and pion+.
        
        Returns:
            Tuple[float, float, float]: Fitted (gamma, delta, epsilon)
        """
        particles = self.create_all_particles()
        
        # Using electron mass to set initial scale
        electron = particles['electron']
        gamma = ParticleData.KNOWN_PARTICLES['electron']['mass'] / len(electron.sub_skbs)
        
        # Using proton and pion+ to fit linking contribution
        proton = particles['proton']
        pion = particles['pion_plus']
        
        A = np.array([
            [proton.get_total_linking_number(), 1],
            [pion.get_total_linking_number(), 1]
        ])
        
        b = np.array([
            ParticleData.KNOWN_PARTICLES['proton']['mass'] - gamma * len(proton.sub_skbs),
            ParticleData.KNOWN_PARTICLES['pion_plus']['mass'] - gamma * len(pion.sub_skbs)
        ])
        
        try:
            delta, epsilon = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            # If system is singular, use simplified model
            delta = 0.0
            epsilon = ParticleData.KNOWN_PARTICLES['electron']['mass']
            
        return gamma, delta, epsilon