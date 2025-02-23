from analysis import ModelAnalyzer

def main():
    # Create analyzer with initial parameters
    analyzer = ModelAnalyzer()
    
    print("Initial analysis with default parameters:")
    results = analyzer.analyze_all_particles()
    analyzer.print_analysis(results)
    
    print("\nFitting mass parameters...")
    gamma, delta, epsilon = analyzer.fit_mass_parameters()
    print(f"Fitted parameters:")
    print(f"γ = {gamma:.3f}")
    print(f"δ = {delta:.3f}")
    print(f"ε = {epsilon:.3f}")
    
    print("\nAnalysis with fitted parameters:")
    analyzer = ModelAnalyzer(gamma, delta, epsilon)
    results = analyzer.analyze_all_particles()
    analyzer.print_analysis(results)

if __name__ == "__main__":
    main()
    main()