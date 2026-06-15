import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_asset_paths(
    time_grid: np.ndarray,
    asset_paths: np.ndarray,
    n_paths: int = 50
) -> None:
    """
    Plot a sample of simulated asset paths.

    Parameters
    ----------
    time_grid:
        Time points used in the simulation.

    asset_paths:
        Simulated asset/fund values.

    n_paths:
        Number of paths to display.
    """

    plt.figure(figsize=(10, 6))

    for i in range(min(n_paths, asset_paths.shape[0])):
        plt.plot(time_grid, asset_paths[i], alpha=0.4)

    plt.title("Simulated Asset Paths using Geometric Brownian Motion")
    plt.xlabel("Time in Years")
    plt.ylabel("Asset/Fund Value")
    plt.tight_layout()
    plt.show()


def plot_event_distribution(risk_results: pd.DataFrame) -> None:
    """
    Plot the distribution of competing risk outcomes.
    """

    event_counts = risk_results["Event_Type"].value_counts()

    plt.figure(figsize=(8, 5))
    event_counts.plot(kind="bar")

    plt.title("Distribution of Competing Risk Events")
    plt.xlabel("Event Type")
    plt.ylabel("Number of Simulations")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_discounted_payoff_distribution(cashflow_results: pd.DataFrame) -> None:
    """
    Plot the distribution of discounted payoffs.
    """

    plt.figure(figsize=(9, 5))
    plt.hist(cashflow_results["discounted_payoff"], bins=50)

    plt.title("Distribution of Discounted Payoffs")
    plt.xlabel("Discounted Payoff")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


def plot_average_payoff_by_event(cashflow_results: pd.DataFrame) -> None:
    """
    Plot average discounted payoff by event type.
    """

    average_payoff = (
        cashflow_results
        .groupby("event_type")["discounted_payoff"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    average_payoff.plot(kind="bar")

    plt.title("Average Discounted Payoff by Event Type")
    plt.xlabel("Event Type")
    plt.ylabel("Average Discounted Payoff")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    
def plot_volatility_sensitivity(sensitivity_df: pd.DataFrame) -> None:
    """
    Plot the estimated fair price against different volatility assumptions.
    """

    plt.figure(figsize=(8, 5))

    plt.plot(
        sensitivity_df["volatility"],
        sensitivity_df["fair_price"],
        marker="o"
    )

    plt.title("Sensitivity of Fair Price to Asset Volatility")
    plt.xlabel("Volatility")
    plt.ylabel("Estimated Fair Price")
    plt.tight_layout()
    plt.show()   

def plot_lapse_rate_sensitivity(sensitivity_df: pd.DataFrame) -> None:
    """
    Plot the estimated fair price against different lapse-rate assumptions.
    """

    plt.figure(figsize=(8, 5))

    plt.plot(
        sensitivity_df["input_lapse_rate"],
        sensitivity_df["fair_price"],
        marker="o"
    )

    plt.title("Sensitivity of Fair Price to Lapse Rate")
    plt.xlabel("Annual Lapse Rate")
    plt.ylabel("Estimated Fair Price")
    plt.tight_layout()
    plt.show()    