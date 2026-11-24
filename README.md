# Macao GGR and Inbound Visitor Arrivals — Regime-Aware Forecast Evaluation (2019–2025)

**CISC7204 Data Science and Data Visualization · Class L · Team 02 · Semester Project**

This repository contains the reproducible analysis, datasets, figures and Dash demo for the team
final project. The written report, presentation deck and storytelling video are submitted separately
on UMMoodle.

**Public repository:** <https://github.com/Yudan-Huang/macao-ggr-visitors-forecast>

## Start here

1. **`READABILITY_STATEMENT.md`** — reading order, file map, key terms, data provenance, reproducibility checklist, and what the project does / does not claim.
2. **`CISC7204_Assignment02_84m.ipynb`** — the main analysis. Run `Kernel → Restart & Run All` from this folder.
3. **`PRESENTATION_PLAN.md`** — presentation plan: opening + correlation, figure-by-figure analysis, technical/Dash/closing.
4. **`dash_app.py` + `README_DASH.md`** — live Dash demo; run `python dash_app.py` and open <http://127.0.0.1:8050>.
5. **`requirements.txt`** — Python dependencies for the notebook and Dash app.

## Main result in one paragraph

The 84-month panel is clean and official. Pooling all 84 months makes every model fail out of sample
(test R² negative), because the sample mixes pre-COVID, pandemic and reopening regimes; Chow tests
reject a single relationship at 2020-02 and 2023-01. The training-window length is then selected on
**2024 validation data only** (2025 is untouched): 24 months has the lowest validation RMSE (1,888.7).
Refit on 2023-03..2025-02, it gives 2025 test R² **0.658**, RMSE **941.6**, MAE **832.9** — essentially
the same R² as the original 48-month Model 4 (0.666 / 929 / 755), though slightly worse on RMSE/MAE.
A rolling one-step backtest over 2024-2025 is more conservative: RMSE **1,967.6**, MAE **1,430.5**;
it beats seasonal naive but is not significantly better than last value. The 84-month extension is
therefore a **regime diagnostic / stress test**, not a claim that more data buys a higher R².

## Dataset requirement (at least two datasets)

The project satisfies the "at least two datasets" requirement with **three primary datasets from two independent official providers**, plus one validation source:

| # | Dataset | Provider | Role in the project |
|---|---|---|---|
| 1 | Monthly gross gaming revenue, 2019-2025 | DICJ | target variable (GGR) |
| 2 | Monthly total inbound arrivals, 2019-2025 | MGTO Data+ | main explanatory variable |
| 3 | Monthly arrivals by 28 source markets, 2019-2025 | MGTO Data+ | market heterogeneity (Model 2, EDA) |
| 4 | Annual tourism/GGR totals | DSEC / DICJ | external validation only, not a model input |

Datasets 1-3 are separate raw files and are merged into one monthly panel for analysis; this is normal data integration, not a replacement for having multiple sources. If the requirement counts independent publishers, DICJ and MGTO are already two; DSEC is a third validation source.

**Source links**

- DICJ: <https://www.dicj.gov.mo/web/en/information/DadosEstat_mensal/index.html>
- MGTO Data+: <https://dataplus.macaotourism.gov.mo/?lang=E>
- DSEC: <https://www.dsec.gov.mo/en-US/Statistic?id=401>

## Data

- `data/raw/income_2019_2025.csv` — DICJ monthly GGR
- `data/raw/visitors_total_2019_2025.csv` — MGTO total arrivals
- `data/raw/visitors_by_market_2019_2025.csv` — MGTO arrivals by 28 source markets
- `data/processed/panel_84m.csv` — pre-built cleaned panel (synced with the notebook output)
- `data_dictionary_84m.csv` — variable definitions, units and sources

## Outputs

- `figures/fig1_trend_84m.png` ... `figures/fig8_residuals.png` — 8 notebook-generated figures
- `gambling_visitors_cleaned.csv` — cleaned 84-month panel
