import numpy as np
from scipy.stats import norm

from src.config import MarketConfig, ProductConfig, SimulationConfig


def black_scholes_put_price(
    spot_price: float,
    strike_price: float,
    risk_free_rate: float,
    volatility: float,
    time_to_maturity: float
) -> float:
    """
    Calculate the Black-Scholes price of a European put option.

    In this project, the put option represents the value of the embedded
    maturity guarantee.

    The maturity benefit is:

        max(S_T, G)

    This can be rewritten as:

        S_T + max(G - S_T, 0)

    So the guarantee component behaves like a European put option with
    strike price G.
    """

    d1 = (
        np.log(spot_price / strike_price)
        + (risk_free_rate + 0.5 * volatility ** 2) * time_to_maturity
    ) / (volatility * np.sqrt(time_to_maturity))

    d2 = d1 - volatility * np.sqrt(time_to_maturity)

    put_price = (
        strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2)
        - spot_price * norm.cdf(-d1)
    )

    return put_price


def guaranteed_maturity_benchmark(
    market_config: MarketConfig,
    product_config: ProductConfig,
    sim_config: SimulationConfig
) -> dict:
    """
    Calculate a Black-Scholes benchmark for the maturity guarantee.

    This benchmark ignores death, lapse, and disability.
    It only values the maturity payoff:

        max(S_T, G)

    Therefore, it is not a replacement for the full insurance pricing engine.
    It is used as a finance benchmark for the embedded guarantee.
    """

    put_value = black_scholes_put_price(
        spot_price=market_config.initial_asset_price,
        strike_price=product_config.maturity_guarantee,
        risk_free_rate=market_config.risk_free_rate,
        volatility=market_config.volatility,
        time_to_maturity=sim_config.years
    )

    benchmark_value = market_config.initial_asset_price + put_value

    return {
        "embedded_put_value": put_value,
        "guaranteed_maturity_benchmark": benchmark_value
    }