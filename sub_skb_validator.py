class SubSKB:
    def __init__(self, twist_number: int, generational_parameter: int, color: str):
        """
        Initialize a sub-SKB with topological properties.
        
        Args:
            twist_number (int): Number of half-twists (affects charge).
            generational_parameter (int): Represents the quark generation (1, 2, or 3).
            color (str): Color charge ('red', 'green', 'blue').
        """
        self.twist_number = twist_number
        self.generational_parameter = generational_parameter
        self.color = color

# Store experimental quark data
QUARK_DATA = {
    'up': {'charge': 2/3, 'generation': 1, 'mass_range': (2.0, 2.5)},  # MeV
    'down': {'charge': -1/3, 'generation': 1, 'mass_range': (4.5, 5.0)},
    'charm': {'charge': 2/3, 'generation': 2, 'mass_range': (1270, 1280)},
    'strange': {'charge': -1/3, 'generation': 2, 'mass_range': (90, 100)},
    'top': {'charge': 2/3, 'generation': 3, 'mass_range': (172000, 173000)},
    'bottom': {'charge': -1/3, 'generation': 3, 'mass_range': (4180, 4220)}
}

def check_charge(sub_skb: SubSKB, quark_name: str) -> bool:
    """Check if the sub-SKB's charge matches the quark's charge."""
    predicted_charge = sub_skb.twist_number / 3  # Charge derived from twist number
    actual_charge = QUARK_DATA[quark_name]['charge']
    return predicted_charge == actual_charge

def check_flavor(sub_skb: SubSKB, quark_name: str) -> bool:
    """Check if the generational parameter matches the quark's generation."""
    return sub_skb.generational_parameter == QUARK_DATA[quark_name]['generation']

def check_color(sub_skb: SubSKB) -> bool:
    """Check if the color is valid (red, green, or blue)."""
    return sub_skb.color in ['red', 'green', 'blue']

def compute_mass(sub_skb: SubSKB, gamma: float, epsilon: float) -> float:
    """
    Compute the mass based on the generational parameter.
    Uses a simple linear model: mass = gamma * generational_parameter + epsilon.
    
    Args:
        sub_skb (SubSKB): The sub-SKB object.
        gamma (float): Scaling factor for generational parameter.
        epsilon (float): Mass offset.
    
    Returns:
        float: Computed mass in MeV.
    """
    return gamma * sub_skb.generational_parameter + epsilon

def check_mass(sub_skb: SubSKB, quark_name: str, gamma: float, epsilon: float) -> bool:
    """Check if the computed mass falls within the quark's mass range."""
    predicted_mass = compute_mass(sub_skb, gamma, epsilon)
    mass_range = QUARK_DATA[quark_name]['mass_range']
    return mass_range[0] <= predicted_mass <= mass_range[1]

def check_topological_completeness(sub_skb: SubSKB) -> bool:
    """Basic check for topological completeness (valid twist and generational parameter)."""
    return (isinstance(sub_skb.twist_number, int) and
            sub_skb.generational_parameter in [1, 2, 3])

def validate_sub_skb(sub_skb: SubSKB, quark_name: str, gamma: float, epsilon: float) -> dict:
    """
    Validate the sub-SKB against a specific quark using all criteria.
    
    Args:
        sub_skb (SubSKB): The sub-SKB to validate.
        quark_name (str): The name of the quark to match against.
        gamma (float): Parameter for mass calculation.
        epsilon (float): Parameter for mass calculation.
    
    Returns:
        dict: Results of each validation criterion.
    """
    if quark_name not in QUARK_DATA:
        return {'error': f"Unknown quark: {quark_name}"}
    
    results = {
        'charge_match': check_charge(sub_skb, quark_name),
        'flavor_match': check_flavor(sub_skb, quark_name),
        'color_valid': check_color(sub_skb),
        'mass_match': check_mass(sub_skb, quark_name, gamma, epsilon),
        'topological_complete': check_topological_completeness(sub_skb)
    }
    
    # Overall match: all criteria must be True
    results['overall_match'] = all(results.values())
    
    return results

# Example usage
if __name__ == "__main__":
    # Example: Validate a sub-SKB for an up quark
    up_quark_skb = SubSKB(twist_number=2, generational_parameter=1, color='red')

    # Mass calculation parameters (example values, to be fitted or predefined)
    gamma = 1.0  # Scaling factor
    epsilon = 1.0  # Offset

    # Validate the sub-SKB
    results = validate_sub_skb(up_quark_skb, 'up', gamma, epsilon)
    print("Validation results for up quark sub-SKB:")
    for criterion, result in results.items():
        print(f"{criterion}: {result}")