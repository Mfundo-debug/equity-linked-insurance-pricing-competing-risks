import matplotlib.pyplot as plt

from src.config import (
    MarketConfig,
    SimulationConfig,
    InsuranceRiskConfig,
    ProductConfig
)

from src.pricing_engine import run_pricing_engine


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

    product_config = ProductConfig(
        maturity_guarantee=120_000,
        death_benefit=130_000,
        disability_benefit=110_000,
        surrender_charge=0.10
    )

    output = run_pricing_engine(
        market_config=market_config,
        sim_config=sim_config,
        risk_config=risk_config,
        product_config=product_config
    )

    time_grid = output["time_grid"]
    asset_paths = output["asset_paths"]
    risk_results = output["risk_results"]
    cashflow_results = output["cashflow_results"]

    print("Pricing engine completed successfully.")

    print("\nPricing summary:")
    print(output["pricing_summary"])

    print("\nEvent type distribution:")
    print(output["event_distribution"])

    print("\nFirst five product cashflows:")
    print(cashflow_results.head())

    print("\nEstimated fair price of the insurance product:")
    print(f"R{output['fair_price']:,.2f}")

    print("\nMonte Carlo standard error of the fair price estimate:")
    print(f"R{output['standard_error']:,.2f}")

    plt.figure(figsize=(10, 6))

    for i in range(50):
        plt.plot(time_grid, asset_paths[i], alpha=0.4)

    plt.title("Simulated Asset Paths using Geometric Brownian Motion")
    plt.xlabel("Time in Years")
    plt.ylabel("Asset/Fund Value")
    plt.tight_layout()
    plt.show()

    event_counts = risk_results["Event_Type"].value_counts()

    plt.figure(figsize=(8, 5))
    event_counts.plot(kind="bar")

    plt.title("Distribution of Competing Risk Events")
    plt.xlabel("Event Type")
    plt.ylabel("Number of Simulations")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(9, 5))
    plt.hist(cashflow_results["discounted_payoff"], bins=50)

    plt.title("Distribution of Discounted Payoffs")
    plt.xlabel("Discounted Payoff")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()