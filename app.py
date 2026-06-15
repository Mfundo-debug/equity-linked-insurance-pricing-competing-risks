import matplotlib.pyplot as plt
import streamlit as st

from src.config import (
    MarketConfig,
    SimulationConfig,
    InsuranceRiskConfig,
    ProductConfig
)

from src.pricing_engine import run_pricing_engine
from src.black_scholes import guaranteed_maturity_benchmark
from src.model_validation import validate_maturity_guarantee_against_black_scholes

from src.sensitivity_analysis import (
    run_volatility_sensitivity,
    run_lapse_rate_sensitivity,
    run_maturity_guarantee_sensitivity
)


st.set_page_config(
    page_title="Equity-Linked Insurance Pricing Engine",
    page_icon="📈",
    layout="wide"
)
if "model_has_run" not in st.session_state:
    st.session_state.model_has_run = False

if "pricing_output" not in st.session_state:
    st.session_state.pricing_output = None

if "black_scholes_output" not in st.session_state:
    st.session_state.black_scholes_output = None

if "validation_results" not in st.session_state:
    st.session_state.validation_results = None

if "sensitivity_results" not in st.session_state:
    st.session_state.sensitivity_results = None

def plot_asset_paths(time_grid, asset_paths, n_paths=50):
    fig, ax = plt.subplots(figsize=(10, 5))

    for i in range(min(n_paths, asset_paths.shape[0])):
        ax.plot(time_grid, asset_paths[i], alpha=0.35)

    ax.set_title("Simulated Asset Paths using Geometric Brownian Motion")
    ax.set_xlabel("Time in Years")
    ax.set_ylabel("Asset / Fund Value")
    ax.grid(True, alpha=0.3)

    return fig


def plot_event_distribution(risk_results):
    event_counts = risk_results["Event_Type"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 4))
    event_counts.plot(kind="bar", ax=ax)

    ax.set_title("Distribution of Competing Risk Events")
    ax.set_xlabel("Event Type")
    ax.set_ylabel("Number of Simulations")
    ax.tick_params(axis="x", rotation=0)
    ax.grid(True, axis="y", alpha=0.3)

    return fig


def plot_discounted_payoff_distribution(cashflow_results):
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.hist(cashflow_results["discounted_payoff"], bins=50)
    ax.set_title("Distribution of Discounted Payoffs")
    ax.set_xlabel("Discounted Payoff")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.3)

    return fig


def plot_sensitivity_line(df, x_col, y_col, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(df[x_col], df[y_col], marker="o")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)

    return fig


@st.cache_data(show_spinner=False)
def run_cached_pricing_engine(
    initial_asset_price,
    risk_free_rate,
    volatility,
    n_simulations,
    years,
    steps_per_year,
    random_seed,
    death_rate,
    lapse_rate,
    disability_rate,
    maturity_guarantee,
    death_benefit,
    disability_benefit,
    surrender_charge
):
    market_config = MarketConfig(
        initial_asset_price=initial_asset_price,
        risk_free_rate=risk_free_rate,
        volatility=volatility
    )

    sim_config = SimulationConfig(
        n_simulations=n_simulations,
        years=years,
        steps_per_year=steps_per_year,
        random_seed=random_seed
    )

    risk_config = InsuranceRiskConfig(
        death_rate=death_rate,
        lapse_rate=lapse_rate,
        disability_rate=disability_rate
    )

    product_config = ProductConfig(
        maturity_guarantee=maturity_guarantee,
        death_benefit=death_benefit,
        disability_benefit=disability_benefit,
        surrender_charge=surrender_charge
    )

    output = run_pricing_engine(
        market_config=market_config,
        sim_config=sim_config,
        risk_config=risk_config,
        product_config=product_config
    )

    black_scholes_output = guaranteed_maturity_benchmark(
        market_config=market_config,
        product_config=product_config,
        sim_config=sim_config
    )

    validation_results = validate_maturity_guarantee_against_black_scholes(
        asset_paths=output["asset_paths"],
        market_config=market_config,
        product_config=product_config,
        sim_config=sim_config
    )

    return output, black_scholes_output, validation_results


st.title("Equity-Linked Insurance Pricing Engine")
st.markdown(
    """
    This application prices an equity-linked life insurance product using 
    Geometric Brownian Motion, Monte Carlo simulation, Black-Scholes benchmarking,
    and competing risk modelling.
    """
)

st.sidebar.header("Market Assumptions")

initial_asset_price = st.sidebar.number_input(
    "Initial asset value",
    min_value=1_000.0,
    max_value=10_000_000.0,
    value=100_000.0,
    step=5_000.0
)

risk_free_rate = st.sidebar.slider(
    "Risk-free rate",
    min_value=0.00,
    max_value=0.25,
    value=0.08,
    step=0.005,
    format="%.3f"
)

volatility = st.sidebar.slider(
    "Asset volatility",
    min_value=0.01,
    max_value=0.80,
    value=0.22,
    step=0.01,
    format="%.2f"
)

st.sidebar.header("Simulation Settings")

n_simulations = st.sidebar.slider(
    "Number of simulations",
    min_value=1_000,
    max_value=50_000,
    value=10_000,
    step=1_000
)

years = st.sidebar.slider(
    "Contract term in years",
    min_value=1,
    max_value=40,
    value=10,
    step=1
)

steps_per_year = st.sidebar.selectbox(
    "Steps per year",
    options=[1, 4, 12],
    index=2
)

random_seed = st.sidebar.number_input(
    "Random seed",
    min_value=1,
    max_value=999_999,
    value=42,
    step=1
)

st.sidebar.header("Competing Risk Assumptions")

death_rate = st.sidebar.slider(
    "Annual death rate",
    min_value=0.000,
    max_value=0.100,
    value=0.012,
    step=0.001,
    format="%.3f"
)

lapse_rate = st.sidebar.slider(
    "Annual lapse rate",
    min_value=0.000,
    max_value=0.300,
    value=0.045,
    step=0.005,
    format="%.3f"
)

disability_rate = st.sidebar.slider(
    "Annual disability rate",
    min_value=0.000,
    max_value=0.100,
    value=0.008,
    step=0.001,
    format="%.3f"
)

st.sidebar.header("Product Assumptions")

maturity_guarantee = st.sidebar.number_input(
    "Maturity guarantee",
    min_value=1_000.0,
    max_value=20_000_000.0,
    value=120_000.0,
    step=5_000.0
)

death_benefit = st.sidebar.number_input(
    "Death benefit",
    min_value=1_000.0,
    max_value=20_000_000.0,
    value=130_000.0,
    step=5_000.0
)

disability_benefit = st.sidebar.number_input(
    "Disability benefit",
    min_value=1_000.0,
    max_value=20_000_000.0,
    value=110_000.0,
    step=5_000.0
)

surrender_charge = st.sidebar.slider(
    "Surrender charge",
    min_value=0.00,
    max_value=0.50,
    value=0.10,
    step=0.01,
    format="%.2f"
)

run_model = st.sidebar.button("Run pricing model", type="primary")

if run_model:
    with st.spinner("Running stochastic pricing engine..."):
        output, black_scholes_output, validation_results = run_cached_pricing_engine(
            initial_asset_price=initial_asset_price,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            n_simulations=n_simulations,
            years=years,
            steps_per_year=steps_per_year,
            random_seed=random_seed,
            death_rate=death_rate,
            lapse_rate=lapse_rate,
            disability_rate=disability_rate,
            maturity_guarantee=maturity_guarantee,
            death_benefit=death_benefit,
            disability_benefit=disability_benefit,
            surrender_charge=surrender_charge
        )

    st.session_state.pricing_output = output
    st.session_state.black_scholes_output = black_scholes_output
    st.session_state.validation_results = validation_results
    st.session_state.model_has_run = True
    st.session_state.sensitivity_results = None

if st.session_state.model_has_run:
    output = st.session_state.pricing_output
    black_scholes_output = st.session_state.black_scholes_output
    validation_results = st.session_state.validation_results

    st.success("Pricing model completed successfully.")

    tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(
        [
            "Valuation",
            "Competing Risks",
            "Cashflows",
            "Black-Scholes Validation",
            "Sensitivity Analysis"
        ]
    )    


    with tab_1:
        st.subheader("Pricing Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Estimated Fair Price",
                f"R{output['fair_price']:,.2f}"
            )

        with col2:
            st.metric(
                "Monte Carlo Standard Error",
                f"R{output['standard_error']:,.2f}"
            )

        with col3:
            st.metric(
                "Black-Scholes Benchmark",
                f"R{black_scholes_output['guaranteed_maturity_benchmark']:,.2f}"
            )

        st.dataframe(output["pricing_summary"], use_container_width=True)

        st.pyplot(
            plot_asset_paths(
                time_grid=output["time_grid"],
                asset_paths=output["asset_paths"],
                n_paths=50
            )
        )

    with tab_2:
        st.subheader("Competing Risk Outcomes")

        event_distribution_df = (
            output["event_distribution"]
            .reset_index()
        )
        event_distribution_df.columns = ["event_type", "percentage"]

        st.dataframe(event_distribution_df, use_container_width=True)

        st.pyplot(
            plot_event_distribution(
                risk_results=output["risk_results"]
            )
        )

    with tab_3:
        st.subheader("Product Cashflows")

        st.dataframe(
            output["cashflow_results"].head(100),
            use_container_width=True
        )

        st.pyplot(
            plot_discounted_payoff_distribution(
                cashflow_results=output["cashflow_results"]
            )
        )

        csv_data = output["cashflow_results"].to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download cashflow results as CSV",
            data=csv_data,
            file_name="cashflow_results.csv",
            mime="text/csv"
        )

    with tab_4:
        st.subheader("Black-Scholes Benchmark and Validation")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Embedded Guarantee Value",
                f"R{black_scholes_output['embedded_put_value']:,.2f}"
            )

        with col2:
            st.metric(
                "Guaranteed Maturity Benchmark",
                f"R{black_scholes_output['guaranteed_maturity_benchmark']:,.2f}"
            )

        st.dataframe(validation_results, use_container_width=True)

        st.markdown(
            """
            The validation compares the Monte Carlo maturity guarantee value 
            against the Black-Scholes analytical benchmark. The full insurance 
            price is different because it also includes death, lapse, disability,
            and surrender value outcomes.
            """
        )

    with tab_5:
        st.subheader("Sensitivity Analysis")

        run_sensitivity = st.button("Run sensitivity analyses")

        if run_sensitivity:
            market_config = MarketConfig(
                initial_asset_price=initial_asset_price,
                risk_free_rate=risk_free_rate,
                volatility=volatility
            )

            sim_config = SimulationConfig(
                n_simulations=n_simulations,
                years=years,
                steps_per_year=steps_per_year,
                random_seed=random_seed
            )

            risk_config = InsuranceRiskConfig(
                death_rate=death_rate,
                lapse_rate=lapse_rate,
                disability_rate=disability_rate
            )

            product_config = ProductConfig(
                maturity_guarantee=maturity_guarantee,
                death_benefit=death_benefit,
                disability_benefit=disability_benefit,
                surrender_charge=surrender_charge
            )

            with st.spinner("Running sensitivity analyses..."):
                volatility_values = [0.10, 0.15, 0.20, volatility, 0.25, 0.30, 0.35]
                volatility_values = sorted(set(volatility_values))

                volatility_sensitivity_df = run_volatility_sensitivity(
                    volatility_values=volatility_values,
                    market_config=market_config,
                    sim_config=sim_config,
                    risk_config=risk_config,
                    product_config=product_config
                )

                lapse_rate_values = [0.01, 0.025, lapse_rate, 0.06, 0.08, 0.10, 0.12]
                lapse_rate_values = sorted(set(lapse_rate_values))

                lapse_sensitivity_df = run_lapse_rate_sensitivity(
                    lapse_rate_values=lapse_rate_values,
                    market_config=market_config,
                    sim_config=sim_config,
                    risk_config=risk_config,
                    product_config=product_config
                )

                guarantee_values = [
                    maturity_guarantee * 0.80,
                    maturity_guarantee * 0.90,
                    maturity_guarantee,
                    maturity_guarantee * 1.10,
                    maturity_guarantee * 1.20,
                    maturity_guarantee * 1.30
                ]

                guarantee_sensitivity_df = run_maturity_guarantee_sensitivity(
                    guarantee_values=guarantee_values,
                    market_config=market_config,
                    sim_config=sim_config,
                    risk_config=risk_config,
                    product_config=product_config
                )

            st.markdown("### Volatility Sensitivity")
            st.dataframe(volatility_sensitivity_df, use_container_width=True)
            st.pyplot(
                plot_sensitivity_line(
                    df=volatility_sensitivity_df,
                    x_col="volatility",
                    y_col="fair_price",
                    title="Sensitivity of Fair Price to Asset Volatility",
                    xlabel="Volatility",
                    ylabel="Estimated Fair Price"
                )
            )

            st.markdown("### Lapse Rate Sensitivity")
            st.dataframe(lapse_sensitivity_df, use_container_width=True)
            st.pyplot(
                plot_sensitivity_line(
                    df=lapse_sensitivity_df,
                    x_col="input_lapse_rate",
                    y_col="fair_price",
                    title="Sensitivity of Fair Price to Lapse Rate",
                    xlabel="Annual Lapse Rate",
                    ylabel="Estimated Fair Price"
                )
            )

            st.markdown("### Maturity Guarantee Sensitivity")
            st.dataframe(guarantee_sensitivity_df, use_container_width=True)
            st.pyplot(
                plot_sensitivity_line(
                    df=guarantee_sensitivity_df,
                    x_col="maturity_guarantee",
                    y_col="fair_price",
                    title="Sensitivity of Fair Price to Maturity Guarantee",
                    xlabel="Maturity Guarantee",
                    ylabel="Estimated Fair Price"
                )
            )

else:
    st.info("Set your assumptions in the sidebar, then click 'Run pricing model'.")