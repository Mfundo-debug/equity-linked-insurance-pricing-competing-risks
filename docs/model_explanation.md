# Model Explanation

This document explains the modelling logic behind the stochastic insurance pricing engine.

The project prices an equity-linked life insurance product using a combination of:

* Geometric Brownian Motion
* Monte Carlo simulation
* Discounted cashflow valuation
* Competing risks
* Black-Scholes benchmarking
* Sensitivity analysis

The objective is to estimate the fair value of an insurance product whose benefits depend on both market performance and policyholder events.

---

## 1. Product Being Modelled

The product is an equity-linked insurance contract.

The policyholder is exposed to an investment fund. The fund value changes over time according to a stochastic market process. At the same time, the policyholder may experience one of several insurance events before the contract matures.

The possible policy outcomes are:

| Outcome    | Description                                                           |
| ---------- | --------------------------------------------------------------------- |
| Death      | The policyholder dies before maturity                                 |
| Lapse      | The policyholder cancels the policy before maturity                   |
| Disability | The policyholder becomes disabled before maturity                     |
| Survival   | The policyholder reaches maturity without death, lapse, or disability |

The first event to occur determines the product payoff.

---

## 2. Market Model

The investment fund is modelled using Geometric Brownian Motion.

The continuous-time model is:

$$ dS_t = rS_tdt + \sigma S_tdW_t $$


where:

| Symbol   | Meaning                 |
| -------- | ----------------------- |
| $S_t$    | Fund value at time $t$  |
| $r$      | Risk-free interest rate |
| $\sigma$ | Asset volatility        |
| $W_t$    | Brownian motion         |

This model assumes that the fund value evolves randomly over time, with uncertainty driven by Brownian motion.

The discrete simulation formula used in the project is:

$$ S_{t+\Delta t} = S_t \exp\left[ \left(r - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t}Z \right] $$

where $Z \sim N(0,1)$.


This allows the model to simulate many possible future fund paths.

---

## 3. Monte Carlo Simulation

Monte Carlo simulation is used because the product payoff depends on uncertain future market values and uncertain insurance events.

The model simulates many possible scenarios. In each scenario:

1. A fund path is simulated using Geometric Brownian Motion.
2. A competing risk event is simulated.
3. The product payoff is calculated.
4. The payoff is discounted back to time zero.
5. The fair price is estimated by averaging all discounted payoffs.

The fair price estimator is:

$$\hat{V} = \frac{1}{N} \sum_{i=1}^{N}e^{-r\tau_i}C_{\tau_i}$$

where:

| Symbol       | Meaning                              |
| ------------ | ------------------------------------ |
| $N$          | Number of simulations                |
| $\tau_i$     | Event time in simulation $i$         |
| $C_{\tau_i}$ | Cashflow paid at event time $\tau_i$ |
| $r$          | Risk-free rate                       |
| $\hat{V}$    | Estimated fair value                 |

---

## 4. Competing Risks Model

The insurance component uses a competing risks framework.

The model includes three active decrements:

* Death
* Lapse
* Disability

If none of these events occurs before maturity, the policyholder is treated as having survived to maturity.

The total competing risk intensity is:

$$\lambda_{\text{total}} = \lambda_{\text{death}} + \lambda_{\text{lapse}} + \lambda_{\text{disability}}$$

The probability that any event occurs during a small time interval $\Delta t$ is:

$$p_{\text{event}} = 1 - e^{-\lambda_{\text{total}}\Delta t}$$

If an event occurs, the event type is selected using relative weights.

For death:

$$P(\text{Death} \mid \text{Event}) = \frac{\lambda_{\text{death}}}{\lambda_{\text{total}}}$$

For lapse:

$$P(\text{Lapse} \mid \text{Event}) = \frac{\lambda_{\text{lapse}}}{\lambda_{\text{total}}}$$

For disability:

$$P(\text{Disability} \mid \text{Event}) = \frac{\lambda_{\text{disability}}}{\lambda_{\text{total}}}$$

This means the first event to occur determines the policy outcome.

---

## 5. Product Payoff Logic

The payoff depends on the simulated event type.

### Death payoff

If death occurs before maturity, the payoff is:

$$C_{\tau} = \max(B_{\text{death}}, S_{\tau})$$

where:

* $B_{\text{death}}$ is the death benefit
* $S_{\tau}$ is the fund value at death time

### Lapse payoff

If lapse occurs before maturity, the payoff is the surrender value:

$$C_{\tau} = S_{\tau}(1 - q)$$

where:

* $q$ is the surrender charge
* $S_{\tau}$ is the fund value at lapse time

### Disability payoff

If disability occurs before maturity, the payoff is:

$$C_{\tau} = \max(B_{\text{disability}}, S_{\tau})$$

where:

* $B_{\text{disability}}$ is the disability benefit
* $S_{\tau}$ is the fund value at disability time

### Survival payoff

If the policyholder survives to maturity, the payoff is:

$$C_T = \max(S_T, G)$$

where:

* $S_T$ is the fund value at maturity
* $G$ is the guaranteed maturity amount

---

## 6. Discounting

Each payoff is discounted back to the present using the risk-free rate.

The discounted payoff is:

$$PV = e^{-r\tau}C_{\tau}$$

where:

| Symbol     | Meaning                     |
| ---------- | --------------------------- |
| $PV$       | Present value of the payoff |
| $r$        | Risk-free rate              |
| $\tau$     | Event time                  |
| $C_{\tau}$ | Cashflow at event time      |

The final fair price is the average of all simulated present values.

---

## 7. Embedded Guarantee Interpretation

The maturity payoff is:

$$\max(S_T, G)$$

This can be rewritten as:

$$\max(S_T, G) = S_T + \max(G - S_T, 0)$$

The second term,

$$\max(G - S_T, 0)$$

is equivalent to a European put option with strike price $G$.

This means the maturity guarantee has option-like behaviour. When the fund value falls below the guarantee, the guarantee becomes valuable.

---

## 8. Black-Scholes Benchmark

The project includes a Black-Scholes benchmark for the embedded maturity guarantee.

The Black-Scholes put option value is:

$$P = G e^{-rT}N(-d_2)S_0N(-d_1)$$

where:

$$d_1 = \frac{\ln\left(\frac{S_0}{G}\right)+\left(r + \frac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}}$$

and:

$$d_2 = d_1 - \sigma\sqrt{T}$$

The guaranteed maturity benchmark is:

$$V_{\text{benchmark}} = S_0 + P$$

This benchmark only values the maturity guarantee. It does not include death, lapse, disability, or surrender benefits.

---

## 9. Model Validation

The Monte Carlo maturity guarantee value is compared against the Black-Scholes benchmark.

This validation ignores competing risks and focuses only on:

$$\max(S_T, G)$$

The purpose is to check whether the simulated market model behaves consistently with the analytical Black-Scholes result.

In the current model output, the Monte Carlo maturity guarantee value is close to the Black-Scholes benchmark, with a small percentage difference. This provides evidence that the simulation engine is working as expected.

---

## 10. Sensitivity Analysis

The project includes sensitivity analysis for key assumptions.

### Volatility sensitivity

The fair price increases as asset volatility increases.

This happens because the maturity guarantee behaves like an embedded put option. Higher volatility increases the probability of extreme market outcomes, which increases the value of the guarantee.

### Lapse-rate sensitivity

The fair price decreases as the lapse rate increases.

This happens because more policyholders exit the contract early and receive surrender values instead of reaching maturity and receiving the maturity guarantee.

### Maturity guarantee sensitivity

The fair price increases as the maturity guarantee increases.

This happens because a higher guarantee increases the insurer’s expected future liability, especially in scenarios where the fund value underperforms.

---

## 11. Key Assumptions

The model uses simplified assumptions for educational and portfolio purposes.

Important assumptions include:

* Constant risk-free interest rate
* Constant asset volatility
* Constant death, lapse, and disability intensities
* No expenses
* No taxes
* No profit loading
* No policy fees
* No dynamic policyholder behaviour
* No calibrated mortality or lapse table
* No regulatory capital or reserving framework

These assumptions make the model easier to understand and implement, but they would need to be expanded for real-world actuarial pricing.

---

## 12. Summary

The model combines financial and actuarial modelling in one pricing framework.

The financial side simulates stochastic fund values using Geometric Brownian Motion.

The insurance side simulates policyholder outcomes using competing risks.

The pricing engine combines both components by calculating discounted cashflows under each simulated scenario.

The project demonstrates how Python can be used to build a practical stochastic pricing model for an equity-linked insurance product.
