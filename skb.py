import numpy as np
from typing import List, Tuple

class SubSKB:
    """Represents a sub-SKB component with a twist number."""
    def __init__(self, twist_number: int):
        """
        Initialize a sub-SKB with a twist number.
        
        Args:
            twist_number (int): Number of half-twists (positive or negative)
        """
        self.twist_number = twist_number
    
    def get_charge(self) -> float:
        """Calculate charge from twist number (charge = twist_number/3)."""
        return self.twist_number / 3

class SKB:
    """
    Represents a Spacetime Klein Bottle (SKB) composed of sub-SKBs.
    Includes topological invariants like twist numbers and linking numbers.
    """
    def __init__(self, sub_skbs: List[SubSKB]):
        """
        Initialize an SKB with a list of sub-SKBs.
        
        Args:
            sub_skbs (List[SubSKB]): List of sub-SKB components
        """
        self.sub_skbs = sub_skbs
        n = len(sub_skbs)
        # Initialize linking numbers matrix (skew-symmetric)
        self.linking_numbers = np.zeros((n, n))
    
    def set_linking_number(self, i: int, j: int, value: int) -> None:
        """
        Set the linking number between two sub-SKBs.
        Maintains skew-symmetry: linking_numbers[j,i] = -linking_numbers[i,j]
        
        Args:
            i, j (int): Indices of sub-SKBs
            value (int): Linking number between sub-SKBs i and j
        """
        if i >= len(self.sub_skbs) or j >= len(self.sub_skbs) or i < 0 or j < 0:
            raise ValueError("Invalid sub-SKB index")
        if i != j:
            self.linking_numbers[i, j] = value
            self.linking_numbers[j, i] = -value
    
    def get_total_twist_number(self) -> int:
        """Calculate total twist number (sum of sub-SKB twist numbers)."""
        return sum(skb.twist_number for skb in self.sub_skbs)
    
    def get_total_linking_number(self) -> int:
        """Calculate total linking number (sum of upper triangle)."""
        return int(np.sum(np.triu(self.linking_numbers)))
    
    def get_charge(self) -> float:
        """Calculate total charge (total twist number / 3)."""
        return self.get_total_twist_number() / 3
    
    def get_mass(self, gamma: float, delta: float, epsilon: float) -> float:
        """
        Calculate mass using the linear model:
        mass = γ * num_sub_skbs + δ * total_linking_number + ε
        
        Args:
            gamma, delta, epsilon: Parameters of the mass function
        """
        return (gamma * len(self.sub_skbs) + 
                delta * self.get_total_linking_number() + 
                epsilon)

def create_particle(name: str, twist_numbers: List[int], 
                   linking_pairs: List[Tuple[int, int, int]]) -> SKB:
    """Create an SKB configuration for a specific particle."""
    sub_skbs = [SubSKB(t) for t in twist_numbers]
    skb = SKB(sub_skbs)
    for i, j, value in linking_pairs:
        skb.set_linking_number(i, j, value)
    return skb

# Predefined particle configurations
PARTICLE_CONFIGS = {
    'proton': {
        'twist_numbers': [2, 2, -1],
        'linking_pairs': [(0,1,1), (1,2,1), (0,2,1)]
    },
    'neutron': {
        'twist_numbers': [1, 1, 1],
        'linking_pairs': [(0,1,1), (1,2,1), (0,2,1)]
    },
    'pion_plus': {
        'twist_numbers': [2, 1],
        'linking_pairs': [(0,1,1)]
    },
    'electron': {
        'twist_numbers': [-3],
        'linking_pairs': []
    },
    'muon': {
        'twist_numbers': [-3],
        'linking_pairs': []
    }
}