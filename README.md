# Doomsday Model

A multi-domain probabilistic threat engine that estimates global danger-state dynamics from structured data and real-time event feeds. It is designed as a transparent, reproducible alternative to purely symbolic risk indicators such as the Bulletin of the Atomic Scientists' Doomsday Clock.

The project does **not** claim that historical data can directly reveal existential-catastrophe probability. Instead, it separates the problem into two parts:

1. **Danger-state probability**, learned from observed signals and historical escalation events.
2. **Catastrophe probability conditional on danger state**, represented with explicit Bayesian priors, scenario assumptions, and uncertainty intervals.

This distinction is the core of the model.

---

## What the model actually estimates

For each domain $d$, define:

```math
D_d = \text{domain } d \text{ enters severe danger / escalation state within horizon } T
```

```math
C_d = \text{domain } d \text{ experiences catastrophe within horizon } T
```

The target is decomposed as:

```math
P(C_d \mid \mathcal F_t)
=
P(D_d \mid \mathcal F_t)
\cdot
P(C_d \mid D_d, \mathcal F_t)
```

where $\mathcal F_t$ is the information available at time $t$.

### 1. Danger-state probability

```math
P(D_d \mid \mathcal F_t)
```

This is the data-driven part. Historical crises, close calls, escalation episodes, conflict events, disease outbreaks, climate indicators, and capability milestones can help infer the probability of entering severe danger states.

This layer is estimated with:

- Hawkes processes for event-driven escalation.
- Hidden Markov Models for latent structural state.
- Continuous Bayesian updating as new signals arrive.

### 2. Conditional catastrophe probability

```math
P(C_d \mid D_d, \mathcal F_t)
```

This is not learned directly from historical catastrophe frequency. There are too few true existential or civilizational catastrophes to estimate such rates frequentistically.

Instead, this term is modeled using structured Bayesian priors informed by:

- expert elicitation,
- technical analysis,
- scenario modeling,
- historical near-miss analysis,
- published forecasts and risk estimates.

For example, nuclear close-call data can estimate the rate of entering dangerous nuclear situations. It cannot by itself estimate the probability that a close call proceeds to launch. That conditional failure probability is represented explicitly as an uncertain prior.

---

## How the model works

### Per-domain danger-state estimation

Each domain combines event-driven and structural information.

A **Hawkes process** captures escalation cascades. Geopolitical and nuclear crises cluster: one event can raise the intensity of subsequent events. The process estimates current danger-event intensity, not direct catastrophe probability.

A **Hidden Markov Model** captures slow-moving structural risk. Climate, AI capability accumulation, institutional decay, and preparedness failures often shift gradually through latent states such as stable, elevated, crisis, and critical.

The two components are fused per domain. The weighted fusion is the interpretable baseline:

```math
p_{\text{danger},d}(t)
=
w_1
\left(
1 - e^{-\lambda_{\text{Hawkes},d}(t)\tau}
\right)
+
w_2
\sum_k P(S_t=s_k \mid x_{1:t}) \cdot \text{danger}_k
```

where $w_1 + w_2 = 1$.

A logistic fusion alternative is available when sufficient labeled data exists:

```math
p_{\text{danger},d}(t)
=
\sigma
\left(
a_d + b_d^\top x_d(t) + c_d\log(1+\lambda_d(t)) + \gamma_d^\top P(z_{d,t})
\right)
```

The weighted version is more interpretable. The logistic version is more flexible.

### Conditional catastrophe priors

For domain-state combinations, define:

```math
q_d = P(C_d \mid D_d, \mathcal F_t)
```

This is represented as a prior distribution, often a Beta distribution for bounded probabilities:

```math
q_d \sim \text{Beta}(\alpha_d,\beta_d)
```

The model therefore outputs a distribution over catastrophe probability, not fake precision.

For event-driven domains:

```math
P(C_d \text{ in } [t,t+T])
=
1 -
\exp
\left(
-\int_t^{t+T}
\lambda_{\text{danger},d}(s)q_d(s)\,ds
\right)
```

For structural domains:

```math
P(C_d \mid \mathcal F_t)
=
\sum_k P(S_t=s_k \mid x_{1:t})r_k
```

where $r_k=P(C_d\mid S_t=s_k)$ is a conditional-risk prior.

### Composite risk

The model uses copula-based aggregation to represent dependence between domain risks.

For marginal catastrophe probabilities $p_1,\ldots,p_5$:

```math
P(\text{any catastrophe within } T)
=
1 - C_R(1-p_1,\ldots,1-p_5)
```

where $C_R$ is a copula over the survival probabilities.

The Gaussian copula is the baseline. A t-copula is preferred for tail-risk modeling because it can represent stronger dependence in extreme states. Dynamic Conditional Correlation can allow the dependence matrix to tighten during simultaneous crises.

The model also computes a severity-weighted systemic risk index:

```math
P\left(\sum_d w_dY_d > \tau\right)
```

where $Y_d$ are correlated latent domain severities. This captures systemic civilizational stress better than a binary “at least one domain failed” event.

### Clock visualization

The clock maps a normalized composite risk score to minutes-to-midnight. It is a visualization, not the model itself.

In implementation, the display score is clamped to prevent invalid values:

```math
p_{\text{display}}
=
\text{clip}(p_{\text{composite}},p_{\min},1)
```

```math
\text{minutes}
=
15\cdot
\frac{\log(1/p_{\text{display}})}{\log(1/p_{\min})}
```

where $p_{\min}$ is the safest historical baseline.

---

## Model outputs

The model produces three distinct outputs.

### 1. Danger-state probabilities

These are data-driven and calibratable.

Example:

> Probability that the nuclear domain enters severe escalation within 12 months: 18.3%.

### 2. Catastrophe posteriors

These are prior-dependent and reported with uncertainty intervals.

Example:

> Nuclear catastrophe probability within 12 months: median 0.3%, 90% credible interval [0.02%, 1.1%].

The exact value depends on the conditional-risk prior $q$, which is explicit and adjustable.

### 3. Composite systemic risk index

This is a 0–100 index used for the dashboard and clock visualization. It is not necessarily a literal probability.

---

## Data sources

All sources are publicly accessible. No proprietary datasets are required.

### Continuous signals

- NOAA Mauna Loa CO₂, 1958–present.
- NASA GISS temperature anomaly, 1880–present.
- Our World in Data / FAS nuclear warhead estimates, 1945–present.
- SIPRI arms transfers and military expenditure, 1949/1950–present depending on dataset.
- NSIDC Arctic sea ice extent, satellite era from 1978–present.
- Epoch AI notable/frontier model data.
- UCDP/PRIO armed conflict data, 1946–present.
- V-Dem democracy and institutional indicators.

### Event feeds

- GDELT, media-derived global event database, historical archives back to 1979, updated every 15 minutes.
- ACLED, curated political violence and protest data, full global real-time coverage since 2022, with region-dependent historical coverage before then.
- WHO Disease Outbreak News.
- ProMED pathogen alerts.

### Important data caveats

GDELT is a media-derived signal source, not ground truth. Media volume does not linearly map to real-world severity. Deduplication and media-bias correction are mandatory.

ACLED coverage varies historically by region. Comparisons before global real-time coverage require region/date-aware normalization.

FAS/OWID warhead counts are estimates because exact nuclear stockpiles are classified.

Epoch AI model data is selection-biased toward notable, published, or otherwise disclosed models. Classified and internal frontier development may be missing.

---

## Validation and calibration

### Danger-state backtesting

The model is run historically using only information available at each time step. It should spike during known danger periods such as the Cuban Missile Crisis, Able Archer 83, and post-2014 geopolitical deterioration, and subside during détente periods.

Evaluation metrics:

- Brier score.
- Log score.
- Reliability diagrams.
- Calibration curves.
- Out-of-time validation.

### Probability calibration

PIT is appropriate for continuous predictive distributions. For rare binary danger-state targets, PIT should be used alongside reliability diagrams, Brier decomposition, log score, and threshold-event backtesting.

### Expert anchoring

Catastrophe posteriors and conditional-risk priors are sanity-checked against:

- Metaculus community forecasts,
- Toby Ord's estimates in *The Precipice*,
- superforecaster surveys,
- domain expert elicitation.

BAS Doomsday Clock positions are used only as coarse historical alignment targets, not ground truth.

---

## Comparison with the BAS Doomsday Clock

| | BAS Clock | Doomsday Model |
|---|---:|---:|
| Update frequency | Annual | Continuous / scheduled |
| Methodology | Expert panel statement | Hawkes + HMM + copula + Bayesian priors |
| Transparency | Qualitative | Open specification |
| Reproducibility | No | Same inputs produce same outputs |
| Probability target | Undefined | Danger state × conditional catastrophe risk |
| Uncertainty quantification | None | Credible intervals |
| Correlation modeling | Informal | Copula / tail dependence |
| Calibration | None published | Brier, log score, PIT, reliability diagrams |

---

## Quickstart

```bash
git clone https://github.com/YOUR_USERNAME/doomsday-model.git
cd doomsday-model
pip install -e .

# Download core datasets
python -m src.ingestion.download --all

# Run historical retrodiction
python -m src.backtest.retrodiction --start 1945 --end 2025

# Launch dashboard
cd dashboard && npm install && npm run dev
```

Requires Python 3.10+ and Node 18+. GDELT BigQuery access requires a Google Cloud account. ACLED requires free academic registration.

---

## Current status

The dashboard prototype is complete with simulated data. The real modeling and ingestion pipeline are under active development.

---

## Contributing

Contributions are welcome in stochastic processes, Bayesian inference, NLP, data engineering, frontend development, and domain expertise across nuclear policy, climate science, biosecurity, AI safety, and international relations.

---

## License

MIT
