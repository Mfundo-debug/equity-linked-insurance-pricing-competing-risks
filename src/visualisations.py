from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def save_figure(save_path: str | None) -> None:
    """
    Save the current matplotlib figure if a save path is provided.
    """

    if save_path is not None:
        output_path = Path(save_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")


def plot_asset_paths(
    time_grid: np.ndarray,
    asset_paths: np.ndarray,
    n_paths: int = 50,
    save_path: str | None = None
) -> None:
    """
    Plot a sample of simulated asset paths.
    """

    plt.figure(figsize=(10, 6))

    for i in range(min(n_paths, asset_paths.shape[0])):
        plt.plot(time_grid, asset_paths[i], alpha=0.4)

    plt.title("Simulated Asset Paths using Geometric Brownian Motion")
    plt.xlabel("Time in Years")
    plt.ylabel("Asset/Fund Value")
    plt.tight_layout()

    save_figure(save_path)
    plt.show()


def plot_event_distribution(
    risk_results: pd.DataFrame,
    save_path: str | None = None
) -> None:
    """
    Plot the distribution of competing risk outcomes.
    """

    event_counts = risk_results["event_type"].value_counts()

    plt.figure(figsize=(8, 5))
    event_counts.plot(kind="bar")

    plt.title("Distribution of Competing Risk Events")
    plt.xlabel("Event Type")
    plt.ylabel("Number of Simulations")
    plt.xticks(rotation=0)
    plt.tight_layout()

    save_figure(save_path)
    plt.show()


def plot_discounted_payoff_distribution(
    cashflow_results: pd.DataFrame,
    save_path: str | None = None
) -> None:
    """
    Plot the distribution of discounted payoffs.
    """

    plt.figure(figsize=(9, 5))
    plt.hist(cashflow_results["discounted_payoff"], bins=50)

    plt.title("Distribution of Discounted Payoffs")
    plt.xlabel("Discounted Payoff")
    plt.ylabel("Frequency")
    plt.tight_layout()

    save_figure(save_path)
    plt.show()


def plot_average_payoff_by_event(
    cashflow_results: pd.DataFrame,
    save_path: str | None = None
) -> None:
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

    save_figure(save_path)
    plt.show()


def plot_volatility_sensitivity(
    sensitivity_df: pd.DataFrame,
    save_path: str | None = None
) -> None:
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

    save_figure(save_path)
    plt.show()


def plot_lapse_rate_sensitivity(
    sensitivity_df: pd.DataFrame,
    save_path: str | None = None
) -> None:
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

    save_figure(save_path)
    plt.show()


def plot_maturity_guarantee_sensitivity(
    sensitivity_df: pd.DataFrame,
    save_path: str | None = None
) -> None:
    """
    Plot the estimated fair price against different maturity guarantees.
    """

    plt.figure(figsize=(8, 5))

    plt.plot(
        sensitivity_df["maturity_guarantee"],
        sensitivity_df["fair_price"],
        marker="o"
    )

    plt.title("Sensitivity of Fair Price to Maturity Guarantee")
    plt.xlabel("Maturity Guarantee")
    plt.ylabel("Estimated Fair Price")
    plt.tight_layout()

    save_figure(save_path)
    plt.show()