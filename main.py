import matplotlib.pyplot as plt

from src.config import MarketConfig, SimulationConfig
from src.market_model import simulate_brownian_motion, simulate_gbm_paths    

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

    time_grid, brownian_paths = simulate_brownian_motion(sim_config)
    _, asset_paths = simulate_gbm_paths(market_config, sim_config)

    print("Brownian Motion simulation complete.")
    print(f"Shape of Brownian paths: {brownian_paths.shape}")

    print("\n Geometric Brownian Motion simulation complete.")
    print(f"Shape of asset paths: {asset_paths.shape}")

    print("\n First 10 values of the first simulated asset path:")
    print(asset_paths[0, :10])

    plt.figure(figsize=(12, 6))

    for i in range(50):
        plt.plot(time_grid, asset_paths[i], lw=0.5) 
    plt.xlabel("Time in Years")
    plt.ylabel("Asset/Fund value")
    plt.title("Simulated Asset Paths using (Geometric Brownian Motion)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()