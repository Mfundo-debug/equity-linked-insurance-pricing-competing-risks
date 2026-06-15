from src.config import (
    MarketConfig,
    SimulationConfig,
    InsuranceRiskConfig,
    ProductConfig
)

from src.pricing_engine import run_pricing_engine
from src.sensitivity_analysis import(run_volatility_sensitivity,
                                     run_lapse_rate_sensitivity) 
from src.black_scholes import guaranteed_maturity_benchmark 

from src.visualisations import (
    plot_asset_paths,
    plot_event_distribution,
    plot_discounted_payoff_distribution,
    plot_average_payoff_by_event,
    plot_volatility_sensitivity,
    plot_lapse_rate_sensitivity
)


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

    print("Pricing engine completed successfully.")

    print("\nPricing summary:")
    print(output["pricing_summary"])

    print("\nEvent type distribution:")
    print(output["event_distribution"])

    print("\nFirst five product cashflows:")
    print(output["cashflow_results"].head())

    print("\nEstimated fair price of the insurance product:")
    print(f"R{output['fair_price']:,.2f}")

    print("\nMonte Carlo standard error of the fair price estimate:")
    print(f"R{output['standard_error']:,.2f}")

    plot_asset_paths(
        time_grid=output["time_grid"],
        asset_paths=output["asset_paths"],
        n_paths=100
    )

    plot_event_distribution(
        risk_results=output["risk_results"]
    )

    plot_discounted_payoff_distribution(
        cashflow_results=output["cashflow_results"]
    )

    plot_average_payoff_by_event(
        cashflow_results=output["cashflow_results"]
    )
    volatility_values = [0.10, 0.15, 0.20, 0.22, 0.25, 0.30, 0.35]

    sensitivity_df = run_volatility_sensitivity(
        volatility_values=volatility_values,
        market_config=market_config,
        sim_config=sim_config,
        risk_config=risk_config,
        product_config=product_config
    )

    print("\nVolatility sensitivity analysis:")
    print(sensitivity_df)

    plot_volatility_sensitivity(
        sensitivity_df=sensitivity_df
    )

    lapse_rate_values = [0.01, 0.025, 0.045, 0.06, 0.08, 0.10, 0.12]

    lapse_sensitivity_df = run_lapse_rate_sensitivity(
        lapse_rate_values=lapse_rate_values,
        market_config=market_config,
        sim_config=sim_config,
        risk_config=risk_config,
        product_config=product_config
    )

    print("\nLapse rate sensitivity analysis:")
    print(lapse_sensitivity_df)

    plot_lapse_rate_sensitivity(
        sensitivity_df=lapse_sensitivity_df
    )



    black_scholes_output = guaranteed_maturity_benchmark(
        market_config=market_config,
        product_config=product_config,
        sim_config=sim_config
    )

    print("\nBlack-Scholes benchmark:")
    print(f"Embedded guarantee value: R{black_scholes_output['embedded_put_value']:,.2f}")
    print(
        "Guaranteed maturity benchmark: "
        f"R{black_scholes_output['guaranteed_maturity_benchmark']:,.2f}"
    )   
    
   

if __name__ == "__main__":
    main()