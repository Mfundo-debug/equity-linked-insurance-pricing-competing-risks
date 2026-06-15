import numpy as np
import pandas as pd

from src.config import MarketConfig, ProductConfig

def calculate_product_cashflows(
        asset_paths: np.ndarray,
        risk_results: pd.DataFrame, 
        product_config: ProductConfig,
        market_config: MarketConfig
) -> pd.DataFrame:
    """"
    Calculate product payoffs and discounted payoffs for each siumulation.

    The payoff depends on the first event experienced by the policyholder, and the asset value at that time.
    - If the event is "Death", the payoff is the maximum of the asset value and the death benefit.
    - If the event is "Lapse", the payoff is the asset value at the time of lapse.
    - If the event is "Disability", the payoff is the maximum of the asset value and the disability benefit.
    - If the event is "Survival", the payoff is the maximum of the asset value at maturity and the maturity guarantee.


    Parameters
    ---------
    asset_paths:
        matrix of simulated asset price paths, with shape (n_simulations, n_steps + 1).
        Each column corresponds to a time step, and each row represents a single simulation path.   
    risk_results:
        Dataframe containing the event type, event time, and event step for each simulated policyholder.    
    product_config:
        Configuration for the insurance product, including payoff parameters.(assumptions on the product features and benefits)
    market_config:
        Configuration for the market, including discounting parameters.(assumptions on the market conditions, such as interest rates)


    Returns
    --------
    cashflow_results:
        Dataframe containing fund valuue  at event, payoff, discounted factor and discounted payoff for each simulation.
    """
    risk_results = risk_results.copy()

    # this makes the function robust if your columns are capitalized differently.
    risk_results = risk_results.rename(columns={
        "Simulation_ID": "simulation_id",
        "Event_Type": "event_type",
        "Event_Time": "event_time",
        "Event_Step": "event_step"
    })

    cashflows  = []

    for _, row in risk_results.iterrows():
        simulation_id = int(row["simulation_id"])
        event_type = row["event_type"]
        event_time = float(row["event_time"])
        event_step = int(row["event_step"])

        fund_value_at_event = asset_paths[simulation_id, event_step]    

        if event_type == "Death":
            payoff = max(product_config.death_benefit, fund_value_at_event)

        elif event_type == "Lapse": 
            payoff = fund_value_at_event * (1 - product_config.surrender_charge)

        elif event_type == "Disability":
            payoff = max(product_config.disability_benefit, fund_value_at_event)

        elif event_type == "Survival":
            payoff = max(product_config.maturity_guarantee, fund_value_at_event)    

        else:
            raise ValueError(f"Unknown event type: {event_type}")

        discount_factor = np.exp(-market_config.risk_free_rate * event_time)
        discounted_payoff = payoff * discount_factor

        cashflows.append({
            "simulation_id": simulation_id,
            "event_type": event_type,
            "event_time": event_time,
            "event_step": event_step,
            "fund_value_at_event": fund_value_at_event,
            "payoff": payoff,
            "discount_factor": discount_factor,
            "discounted_payoff": discounted_payoff
        })

    cashflow_results = pd.DataFrame(cashflows)
    return cashflow_results