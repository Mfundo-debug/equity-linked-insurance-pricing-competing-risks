from dataclasses import replace
import pandas as pd

from src.config import (
    MarketConfig,
    SimulationConfig,
    InsuranceRiskConfig,
    ProductConfig
)

from src.pricing_engine import run_pricing_engine


def run_volatility_sensitivity(
    volatility_values: list[float],
    market_config: MarketConfig,
    sim_config: SimulationConfig,
    risk_config: InsuranceRiskConfig,
    product_config: ProductConfig
) -> pd.DataFrame:
    """
    Run sensitivity analysis on asset volatility.

    This shows how the estimated fair price changes when the volatility
    assumption changes.

    Higher volatility usually increases the value of embedded guarantees
    because the payoff has option-like behaviour.
    """

    sensitivity_results = []

    for volatility in volatility_values:
        adjusted_market_config = replace(
            market_config,
            volatility=volatility
        )

        output = run_pricing_engine(
            market_config=adjusted_market_config,
            sim_config=sim_config,
            risk_config=risk_config,
            product_config=product_config
        )

        sensitivity_results.append({
            "volatility": volatility,
            "fair_price": output["fair_price"],
            "standard_error": output["standard_error"]
        })

    sensitivity_df = pd.DataFrame(sensitivity_results)

    return sensitivity_df