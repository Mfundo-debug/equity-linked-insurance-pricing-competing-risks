import numpy as np
import pandas as pd

from src.config import InsuranceRiskConfig, SimulationConfig

def simulate_competing_risks(
        risk_config: InsuranceRiskConfig,
        sim_config: SimulationConfig
) -> pd.DataFrame:
    """"
    simulate competing risk outcoes for each policyholder over the simulation period.

    The possible outcomes are:
    - Death
    - Lapse
    - Disability    
    - Survival to maturity

    A competing risk setup means that the first event to occur determines the  policy outcome
    for example, if a policyholder lapses in year 3, they cannot later die uder same activity policy in year 6.

    Returns
    -------
    risk_results:
        Dataframe containing the event type, event time, and event step for each simulated policyholder.
    """

    rng = np.random.default_rng(sim_config.random_seed + 1)

    total_rate = (
        risk_config.death_rate +
        risk_config.lapse_rate +
        risk_config.disability_rate 
    )

    event_probability = 1 - np.exp(-total_rate * sim_config.dt)

    death_weight = risk_config.death_rate / total_rate  
    lapse_weight = risk_config.lapse_rate / total_rate
    disability_weight = risk_config.disability_rate / total_rate

    results = []    

    for simulation_id in range(sim_config.n_simulations):
        event_found = False
        for step in range(1, sim_config.n_steps + 1):
            event_time = step * sim_config.dt

            event_draw = rng.uniform()

            if event_draw < event_probability:
                event_type_draw = rng.uniform()
                if event_type_draw < death_weight:
                    event_type = "Death"
                elif event_type_draw < death_weight + lapse_weight:
                    event_type = "Lapse"
                elif event_type_draw < death_weight + lapse_weight + disability_weight:
                    event_type = "Disability"
                else:
                    event_type = "Survival"

                results.append({
                    "Simulation_ID": simulation_id,
                    "Event_Type": event_type,
                    "Event_Time": event_time,
                    "Event_Step": step
                })
                event_found = True
                break

        if not event_found:
            results.append({
                "Simulation_ID": simulation_id,
                "Event_Type": "Survival",
                "Event_Time": sim_config.years,
                "Event_Step": sim_config.n_steps
            })

    risk_results = pd.DataFrame(results)    
    return risk_results