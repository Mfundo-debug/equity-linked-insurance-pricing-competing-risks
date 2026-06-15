from dataclasses import dataclass

@dataclass
class MarketConfig:
    """
    Configuration for the financial market model.

    initial_asset_price:
        Starting value of the investment fund or asset.

    risk_free_rate:
        Annualized risk-free interest rate, used for discounting future cash flows.

    volatility:
            Annualized volatility of the asset price, representing the degree of variation in returns.
    
    """

    initial_asset_price: float = 100_000
    risk_free_rate: float = 0.08
    volatility: float = 0.22

@dataclass
class SimulationConfig:
    """
    Configuration for the Monte Carlo simulation.

    n_simulations:
        Number of independent simulation runs to perform.   

    years:
        Length of the contract in years

    steps_per_year:
        Number of time steps per year for the simulation, affecting the granularity of the results.
        12 means monthly steps, 252 means daily steps (assuming 252 trading days in a year).
    """
    
    n_simulations: int = 10_000
    years: int = 10
    steps_per_year: int = 12
    random_seed: int = 42

    @property
    def n_steps(self) -> int:
        """Total number of time steps in the simulation."""
        return self.years * self.steps_per_year
    
    @property
    def dt(self) -> float:
        return 1 / self.steps_per_year
    
@dataclass
class InsuranceRiskConfig:
    """"
    Configuration for the insurance competing risks.

    These are annual risk intensities.
    They represet the force/rate at which each event may occur, and are used to model the probability of each event happening over time.
    """

    death_rate: float = 0.0012
    lapse_rate: float = 0.0045
    disability_rate: float = 0.008