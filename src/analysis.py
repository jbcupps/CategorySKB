from typing import Dict, Tuple, List
import numpy as np
from skb import SKB, create_particle, PARTICLE_CONFIGS

class ParticleData:
    """Experimental particle data for comparison."""
    # Mass in MeV/c², charge in e
    KNOWN_PARTICLES = {
        'proton': {'mass': 938.0, 'charge': 1.0},
        'neutron': {'mass': 939.6, 'charge': 0.0},
        'pion_plus': {'mass': 139.6, 'charge': 1.0},
        'electron': {'mass': 0.511, 'charge': -1.0},
        'muon': {'mass': 105.66, 'charge': -1.0}
    }

class ModelAnalyzer:
    """Analyzes SKB model predictions against experimental data."""
    
    def __init__(self, gamma: float = -520.2, delta: float = 659.3, 
                 epsilon: float = 520.711):
        """
        Initialize with mass function parameters.
        Default values from initial fitting.
        """
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
    
    def create_all_particles(self) -> Dict[str, SKB]:
        """Create SKB representations for all configured particles."""
        particles = {}
        for name, config in PARTICLE_CONFIGS.items():
            particles[name] = create_particle(
                name, 
                config['twist_numbers'],
                config['linking_pairs']
            )
        return particles
    
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
            raise ValueError(f"No experimental data for particle: {name}")
            
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
        results = []
        for name, skb in particles.items():
            try:
                result = self.analyze_particle(name, skb)
                results.append(result)
            except ValueError as e:
                print(f"Warning: {e}")
        return results
    
    def fit_mass_parameters(self) -> Tuple[float, float, float]:
        """
        Fit mass function parameters using experimental data.
        Uses a simple system of equations for initial particles.
        
        Returns:
            Tuple[float, float, float]: Fitted (gamma, delta, epsilon)
        """
        particles = self.create_all_particles()
        
        # Create system of equations for electron, proton, and pion+
        # mass = γ * num_sub_skbs + δ * total_linking_number + ε
        A = np.array([
            [1, 0, 1],  # electron: 1 sub-SKB, 0 linking
            [3, 3, 1],  # proton: 3 sub-SKBs, 3 linking
            [2, 1, 1],  # pion+: 2 sub-SKBs, 1 linking
        ])
        
        b = np.array([
            ParticleData.KNOWN_PARTICLES['electron']['mass'],
            ParticleData.KNOWN_PARTICLES['proton']['mass'],
            ParticleData.KNOWN_PARTICLES['pion_plus']['mass']
        ])
        
        # Solve system of equations
        gamma, delta, epsilon = np.linalg.solve(A, b)
        return gamma, delta, epsilon
    
    def print_analysis(self, results: List[Dict]) -> None:
        """Print analysis results in a formatted table."""
        print("\nParticle Analysis Results:")
        print("-" * 80)
        print(f"{'Particle':<10} {'Charge':<20} {'Mass (MeV/c²)':<30} {'Mass Error %':<10}")
        print("-" * 80)
        for r in results:
            print(f"{r['name']:<10} "
                  f"{r['predicted_charge']:>6.2f} vs {r['actual_charge']:<6.2f}  "
                  f"{r['predicted_mass']:>10.3f} vs {r['actual_mass']:<10.3f}  "
                  f"{r['mass_error_percent']:>8.2f}%")
        print("-" * 80)