from pathlib import Path
import pandas as pd


def create_output_directory(output_dir: str = "outputs/results") -> Path:
    """
    Create the output directory if it does not already exist.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path


def export_pricing_outputs(
    pricing_output: dict,
    output_dir: str = "outputs/results"
) -> None:
    """
    Export the main pricing engine outputs to CSV files.
    """

    output_path = create_output_directory(output_dir)

    pricing_output["pricing_summary"].to_csv(
        output_path / "pricing_summary.csv",
        index=False
    )

    pricing_output["risk_results"].to_csv(
        output_path / "risk_results.csv",
        index=False
    )

    pricing_output["cashflow_results"].to_csv(
        output_path / "cashflow_results.csv",
        index=False
    )

    event_distribution_df = (
        pricing_output["event_distribution"]
        .reset_index()
    )

    event_distribution_df.columns = ["event_type", "percentage"]

    event_distribution_df.to_csv(
        output_path / "event_distribution.csv",
        index=False
    )


def export_sensitivity_results(
    volatility_sensitivity_df: pd.DataFrame,
    lapse_sensitivity_df: pd.DataFrame,
    guarantee_sensitivity_df: pd.DataFrame,
    output_dir: str = "outputs/results"
) -> None:
    """
    Export sensitivity analysis results to CSV files.
    """

    output_path = create_output_directory(output_dir)

    volatility_sensitivity_df.to_csv(
        output_path / "volatility_sensitivity.csv",
        index=False
    )

    lapse_sensitivity_df.to_csv(
        output_path / "lapse_rate_sensitivity.csv",
        index=False
    )

    guarantee_sensitivity_df.to_csv(
        output_path / "maturity_guarantee_sensitivity.csv",
        index=False
    )

def export_validation_results(
    validation_results: pd.DataFrame,
    output_dir: str = "outputs/results"
) -> None:
    """
    Export model validation results to CSV.
    """

    output_path = create_output_directory(output_dir)

    validation_results.to_csv(
        output_path / "black_scholes_validation.csv",
        index=False
    )