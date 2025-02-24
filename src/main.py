from analysis import ModelAnalyzer

def main():
    analyzer = ModelAnalyzer()
    print("Initial analysis:")
    results = analyzer.analyze_all_particles()
    for result in results:
        print(result)
    
    print("\nFitting parameters:")
    gamma, delta, epsilon = analyzer.fit_mass_parameters()
    print(f"γ = {gamma:.3f}, δ = {delta:.3f}, ε = {epsilon:.3f}")
    
    analyzer = ModelAnalyzer(gamma, delta, epsilon)
    print("\nUpdated analysis:")
    results = analyzer.analyze_all_particles()
    for result in results:
        print(result)

if __name__ == "__main__":
    main()