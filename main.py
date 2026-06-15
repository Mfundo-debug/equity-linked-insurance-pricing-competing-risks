import matplotlib.pyplot as plt

from src.config import MarketConfig, SimulationConfig
from src.market_model import simulate_brownian_motion, simulate_gbm_paths    
from src.competing_risks import InsuranceRiskConfig, simulate_competing_risks

def main():
    market_config = MarketConfig(
        initial_asset_price=100_000,
        risk_free_rate=0.08,
        volatility=0.22
    )

    sim_config = SimulationConfig(
        n_simulations=10_000,
        years=10,
        steps_per_year=12,
        random_seed=42
    )
    risk_config = InsuranceRiskConfig(
        death_rate=0.012,
        lapse_rate=0.045,
        disability_rate=0.008
    )

    time_grid, brownian_paths = simulate_brownian_motion(sim_config)
    _, asset_paths = simulate_gbm_paths(market_config, sim_config)
    risk_results = simulate_competing_risks(risk_config, sim_config)

    print("Brownian Motion simulation complete.")
    print(f"Shape of Brownian paths: {brownian_paths.shape}")

    print("\n Geometric Brownian Motion simulation complete.")
    print(f"Shape of asset paths: {asset_paths.shape}")

    print("\n First 10 values of the first simulated asset path:")
    print(asset_paths[0, :10])

    print(("\n Competing Risks simulation complete."))
    print(risk_results.head())

    print("\n Event type distribution:")
    print(risk_results['Event_Type'].value_counts(normalize=True).mul(100).round(2))

    plt.figure(figsize=(12, 6))

    for i in range(50):
        plt.plot(time_grid, asset_paths[i], lw=0.5) 
    plt.xlabel("Time in Years")
    plt.ylabel("Asset/Fund value")
    plt.title("Simulated Asset Paths using (Geometric Brownian Motion)")
    plt.tight_layout()
    plt.show()

    event_counts = risk_results['Event_Type'].value_counts()
    plt.figure(figsize=(8, 6)) 
    event_counts.plot(kind='bar')
    plt.xlabel("Event Type")
    plt.ylabel("Number of Simulations")
    plt.title("Distribution of Competing Risk Events")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()