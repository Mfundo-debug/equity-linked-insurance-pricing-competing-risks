import numpy as np
import pandas as pd

from src.config import MarketConfig, ProductConfig, SimulationConfig
from src.black_scholes import guaranteed_maturity_benchmark


def validate_maturity_guarantee_against_black_scholes(
    asset_paths: np.ndarray,
    market_config: MarketConfig,
    product_config: ProductConfig,
    sim_config: SimulationConfig
) -> pd.DataFrame:
    """
    Validate the Monte Carlo maturity guarantee value against the
    Black-Scholes benchmark.

    This validation ignores death, lapse, and disability.

    It only compares the maturity payoff:

        max(S_T, G)

    against the Black-Scholes value of:

        S_0 + embedded put option
    """

    terminal_asset_values = asset_paths[:, -1]

    maturity_payoffs = np.maximum(
        terminal_asset_values,
        product_config.maturity_guarantee
    )

    discounted_maturity_payoffs = maturity_payoffs * np.exp(
        -market_config.risk_free_rate * sim_config.years
    )

    monte_carlo_value = discounted_maturity_payoffs.mean()

    monte_carlo_standard_error = (
        discounted_maturity_payoffs.std()
        / np.sqrt(sim_config.n_simulations)
    )

    black_scholes_output = guaranteed_maturity_benchmark(
        market_config=market_config,
        product_config=product_config,
        sim_config=sim_config
    )

    black_scholes_value = black_scholes_output["guaranteed_maturity_benchmark"]

    absolute_difference = monte_carlo_value - black_scholes_value

    percentage_difference = (
        absolute_difference / black_scholes_value
    ) * 100

    validation_results = pd.DataFrame({
        "Metric": [
            "Monte Carlo Maturity Guarantee Value",
            "Monte Carlo Standard Error",
            "Black-Scholes Benchmark Value",
            "Absolute Difference",
            "Percentage Difference"
        ],
        "Value": [
            monte_carlo_value,
            monte_carlo_standard_error,
            black_scholes_value,
            absolute_difference,
            percentage_difference
        ]
    })

    return validation_results