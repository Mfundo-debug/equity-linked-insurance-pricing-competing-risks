import numpy as np

from src.config import MarketConfig, SimulationConfig

def simulate_brownian_motion(sim_config: SimulationConfig) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate standard Brownian motions paths
    
    Brownian Motion is the random noise process used inside many financials models.

    Returns:
    -------
    time_grid : np.ndarray
        Array of time points corresponding to the simulation steps.
        Array of time points from 0 to T.

    brownian_paths : np.ndarray
        Simulated Brownian motion paths, with shape (n_simulations, n_steps + 1).
        Each row represents a single simulation path, and each column corresponds to a time step.
    """

    rng = np.random.default_rng(sim_config.random_seed)

    time_grid = np.linspace(0, sim_config.years, sim_config.n_steps + 1)

    random_shocks = rng.normal(
        loc=0.0,
        scale=np.sqrt(sim_config.dt), 
        size=(sim_config.n_simulations, sim_config.n_steps)
        )

    brownian_paths= np.zeros((sim_config.n_simulations, sim_config.n_steps + 1))
    brownian_paths[:, 1:] = np.cumsum(random_shocks, axis=1)    

    return time_grid, brownian_paths

def simulate_gbm_paths(
        market_config: MarketConfig,
        sim_config: SimulationConfig
)  -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate Geometric Brownian Motion (GBM) paths for asset prices.

   Geometric Brownian Motion is commonly used in the Black-Scholes model 
   to represent the stochastic behavior of asset prices over time.
   The model is:
   dS_t = r * S_t * dt + sigma * S_t * dW_t
   
   In simulation form:
   S(t+dt) = S_t * exp((r - 0.5 * sigma^2) * dt + sigma *sqrt(dt)*Z)

    Returns
    -------
    time_grid : np.ndarray
        Array of time points corresponding to the simulation steps.
        Array of time points from 0 to T.
    asset_paths:
        matrix of simulated asset price paths, with shape (n_simulations, n_steps + 1).
        Each column corresponds to a time step, and each row represents a single simulation path.
    
    """
    rng = np.random.default_rng(sim_config.random_seed)

    time_grid = np.linspace(0, sim_config.years, sim_config.n_steps + 1)

    asset_paths = np.zeros((sim_config.n_simulations, sim_config.n_steps + 1))
    asset_paths[:, 0] = market_config.initial_asset_price

    for step in range(1, sim_config.n_steps + 1):
        z = rng.normal(loc=0.0, scale=1.0, size=sim_config.n_simulations)

        asset_paths[:, step] = asset_paths[:, step - 1] * np.exp(   
            (market_config.risk_free_rate - 0.5 * market_config.volatility ** 2) * sim_config.dt +
            market_config.volatility * np.sqrt(sim_config.dt) * z
        )

    return time_grid, asset_paths   