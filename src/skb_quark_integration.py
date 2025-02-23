import numpy as np
from typing import List, Tuple, Dict

class SubSKB:
    def __init__(self, twist_number: int, generational_parameter: int, color: str):
        self.twist_number = twist_number
        self.generational_parameter = generational_parameter
        self.color = color
    
    def get_charge(self) -> float:
        return self.twist_number / 3

class SKB:
    def __init__(self, sub_skbs: List[SubSKB]):
        self.sub_skbs = sub_skbs
        n = len(sub_skbs)
        self.linking_numbers = np.zeros((n, n))
    
    def set_linking_number(self, i: int, j: int, value: int) -> None:
        if i >= len(self.sub_skbs) or j >= len(self.sub_skbs) or i < 0 or j < 0:
            raise ValueError("Invalid sub-SKB index")
        if i != j:
            self.linking_numbers[i, j] = value
            self.linking_numbers[j, i] = -value
    
    def get_total_twist_number(self) -> int:
        return sum(skb.twist_number for skb in self.sub_skbs)
    
    def get_total_linking_number(self) -> int:
        return int(np.sum(np.triu(self.linking_numbers)))
    
    def get_charge(self) -> float:
        return self.get_total_twist_number() / 3

QUARK_DATA = {
    'up': {'charge': 2/3, 'generation': 1, 'mass_range': (2.0, 2.5)},
    'down': {'charge': -1/3, 'generation': 1, 'mass_range': (4.5, 5.0)},
    'charm': {'charge': 2/3, 'generation': 2, 'mass_range': (1270, 1280)},
    'strange': {'charge': -1/3, 'generation': 2, 'mass_range': (90, 100)},
    'top': {'charge': 2/3, 'generation': 3, 'mass_range': (172000, 173000)},
    'bottom': {'charge': -1/3, 'generation': 3, 'mass_range': (4180, 4220)}
}

def validate_sub_skb(sub_skb: SubSKB, quark_name: str, gamma: float, epsilon: float) -> Dict[str, bool]:
    results = {
        'charge_match': sub_skb.get_charge() == QUARK_DATA[quark_name]['charge'],
        'flavor_match': sub_skb.generational_parameter == QUARK_DATA[quark_name]['generation'],
        'color_valid': sub_skb.color in ['red', 'green', 'blue'],
        'mass_match': (QUARK_DATA[quark_name]['mass_range'][0] <= 
                       (gamma * sub_skb.generational_parameter + epsilon) <= 
                       QUARK_DATA[quark_name]['mass_range'][1]),
        'topological_complete': isinstance(sub_skb.twist_number, int) and sub_skb.generational_parameter in [1, 2, 3]
    }
    results['overall_match'] = all(results.values())
    return results

def create_particle(name: str, twist_numbers: List[int], generational_params: List[int], 
                   colors: List[str], linking_pairs: List[Tuple[int, int, int]]) -> SKB:
    sub_skbs = [SubSKB(t, g, c) for t, g, c in zip(twist_numbers, generational_params, colors)]
    skb = SKB(sub_skbs)
    for i, j, value in linking_pairs:
        skb.set_linking_number(i, j, value)
    return skb

PARTICLE_CONFIGS = {
    'proton': {
        'twist_numbers': [2, 2, -1],
        'generational_params': [1, 1, 1],
        'colors': ['red', 'green', 'blue'],
        'linking_pairs': [(0, 1, 1), (1, 2, 1), (0, 2, 1)]
    },
    'neutron': {
        'twist_numbers': [2, -1, -1],
        'generational_params': [1, 1, 1],
        'colors': ['red', 'green', 'blue'],
        'linking_pairs': [(0, 1, 1), (1, 2, 1), (0, 2, 1)]
    }
}

# Iteration mechanism
ITERATION_CONFIGS = [
    {'twist_number': 2, 'generational_param': 1, 'color': 'red'},
    {'twist_number': -1, 'generational_param': 1, 'color': 'blue'},
    {'twist_number': 2, 'generational_param': 2, 'color': 'green'}
]