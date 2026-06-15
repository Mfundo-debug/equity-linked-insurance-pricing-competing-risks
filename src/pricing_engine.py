import pandas as pd

from src.config import (
    MarketConfig,
    SimulationConfig,
    InsuranceRiskConfig,
    ProductConfig
)

from src.export_results import export_pricing_outputs
from src.market_model import simulate_brownian_motion, simulate_gbm_paths
from src.competing_risks import simulate_competing_risks
from src.product import calculate_product_cashflows



def run_pricing_engine(
    market_config: MarketConfig,
    sim_config: SimulationConfig,
    risk_config: InsuranceRiskConfig,
    product_config: ProductConfig
) -> dict:
    """
    Run the full stochastic pricing engine.

    The engine combines:
        1. Brownian Motion simulation
        2. Geometric Brownian Motion asset simulation
        3. Competing risk simulation
        4. Product payoff calculation
        5. Discounted cashflow valuation

    Returns
    -------
    pricing_output:
        Dictionary containing all major model outputs.
    """

    time_grid, brownian_paths = simulate_brownian_motion(sim_config)

    _, asset_paths = simulate_gbm_paths(
        market_config=market_config,
        sim_config=sim_config
    )

    risk_results = simulate_competing_risks(
        risk_config=risk_config,
        sim_config=sim_config
    )

    cashflow_results = calculate_product_cashflows(
        asset_paths=asset_paths,
        risk_results=risk_results,
        product_config=product_config,
        market_config=market_config
    )

    fair_price = cashflow_results["discounted_payoff"].mean()

    standard_error = (
        cashflow_results["discounted_payoff"].std()
        / sim_config.n_simulations ** 0.5
    )

    event_distribution = (
        risk_results["Event_Type"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

    pricing_summary = pd.DataFrame({
        "Metric": [
            "Estimated Fair Price",
            "Monte Carlo Standard Error",
            "Number of Simulations",
            "Contract Term",
            "Initial Asset Value",
            "Risk-Free Rate",
            "Volatility"
        ],
        "Value": [
            fair_price,
            standard_error,
            sim_config.n_simulations,
            sim_config.years,
            market_config.initial_asset_price,
            market_config.risk_free_rate,
            market_config.volatility
        ]
    })

    pricing_output = {
        "time_grid": time_grid,
        "brownian_paths": brownian_paths,
        "asset_paths": asset_paths,
        "risk_results": risk_results,
        "cashflow_results": cashflow_results,
        "fair_price": fair_price,
        "standard_error": standard_error,
        "event_distribution": event_distribution,
        "pricing_summary": pricing_summary
    }

    return pricing_output
    

    
