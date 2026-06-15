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


def run_lapse_rate_sensitivity(
    lapse_rate_values: list[float],
    market_config: MarketConfig,
    sim_config: SimulationConfig,
    risk_config: InsuranceRiskConfig,
    product_config: ProductConfig
) -> pd.DataFrame:
    """
    Run sensitivity analysis on the lapse rate.

    This shows how the estimated fair price changes when policyholders
    are more or less likely to cancel the policy before maturity.

    Lapse is important in insurance pricing because it affects whether
    the insurer pays the maturity guarantee, death benefit, disability
    benefit, or surrender value.
    """

    sensitivity_results = []

    for lapse_rate in lapse_rate_values:
        adjusted_risk_config = replace(
            risk_config,
            lapse_rate=lapse_rate
        )

        output = run_pricing_engine(
            market_config=market_config,
            sim_config=sim_config,
            risk_config=adjusted_risk_config,
            product_config=product_config
        )

        event_distribution = output["event_distribution"]

        sensitivity_results.append({
            "input_lapse_rate": lapse_rate,
            "fair_price": output["fair_price"],
            "standard_error": output["standard_error"],
            "survival_percentage": event_distribution.get("Survival", 0),
            "lapse_percentage": event_distribution.get("Lapse", 0),
            "death_percentage": event_distribution.get("Death", 0),
            "disability_percentage": event_distribution.get("Disability", 0)
        })

    sensitivity_df = pd.DataFrame(sensitivity_results)

    return sensitivity_df


def run_maturity_guarantee_sensitivity(
    guarantee_values: list[float],
    market_config: MarketConfig,
    sim_config: SimulationConfig,
    risk_config: InsuranceRiskConfig,
    product_config: ProductConfig
) -> pd.DataFrame:
    """
    Run sensitivity analysis on the maturity guarantee.

    This shows how the estimated fair price changes when the guaranteed
    maturity benefit is increased or decreased.
    """

    sensitivity_results = []

    for guarantee in guarantee_values:
        adjusted_product_config = replace(
            product_config,
            maturity_guarantee=guarantee
        )

        output = run_pricing_engine(
            market_config=market_config,
            sim_config=sim_config,
            risk_config=risk_config,
            product_config=adjusted_product_config
        )

        cashflow_results = output["cashflow_results"]

        survival_cashflows = cashflow_results[
            cashflow_results["event_type"] == "Survival"
        ]

        if "payoff" in survival_cashflows.columns:
            average_survival_payoff = survival_cashflows["payoff"].mean()
        else:
            average_survival_payoff = None

        sensitivity_results.append({
            "maturity_guarantee": guarantee,
            "fair_price": output["fair_price"],
            "standard_error": output["standard_error"],
            "survival_percentage": output["event_distribution"].get("Survival", 0),
            "average_survival_payoff": average_survival_payoff
        })

    sensitivity_df = pd.DataFrame(sensitivity_results)

    return sensitivity_df

